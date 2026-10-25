#!/usr/bin/env python3
"""
kk guard: PreToolUse engine for the secrets-and-destruction guard.

Reads one hook payload from stdin, decides, and either stays silent (allow)
or emits a deny on every channel the harnesses honour:

  stdout  {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                   "permissionDecision": "deny",
                                   "permissionDecisionReason": "<reason>"}}
  stderr  the same reason text
  exit 2

Allowed calls print nothing and exit 0. The engine never emits an allow
decision: the harness evaluates its own deny rules regardless of hook output,
so an allow buys nothing and could only mislead.

The policy lives in `guard-rules.json` next to this file (override with
`KK_GUARD_RULES`). The engine refuses to run against an unknown declaration
`version` and fails closed, so a schema change can never silently match
nothing.

Two directories are kept distinct and never interchanged:

  project root  `KK_GUARD_PROJECT_ROOT`, else `CLAUDE_PROJECT_DIR`, else the
                payload `cwd`. Anchors every project-relative glob.
  exec dir      the payload `cwd`. Relative arguments resolve against it.

Claude Code persists the shell working directory across Bash calls, so the
payload `cwd` is routinely a subdirectory of the root; anchoring globs to it
would let `../.env` read from `<root>/sub` slip past `./**/.env`.

Every check is a pure function that raises `Denied`; only `main` turns that
into output and an exit code, so tests import this module and call the
checks in-process. The module imports nothing outside the standard library
and stays within Python 3.8 syntax.

The wrapper/engine split, the `-I` interpreter flag, the fail-closed exit
contract and the deny-message shape that hands the action back to the human
are borrowed from safe-claude-code (hooks/guard.py). The policy itself,
the glob matcher and the project-root anchoring are this project's own.
"""

import json
import os
import re
import sys

SUPPORTED_VERSIONS = (1,)

FILE_TOOLS = ("Read", "Grep", "Glob", "Edit", "Write", "NotebookEdit")
PATH_KEYS = {
    "Read": ("file_path",),
    "Edit": ("file_path",),
    "Write": ("file_path",),
    "NotebookEdit": ("notebook_path",),
    "Grep": ("path",),
    "Glob": ("path",),
}

REMEDIES = {
    "secrets": (
        "this path is a secret file; ask the user for the value you need, "
        "or for a redacted copy"
    ),
    "destructive": (
        "run it yourself by typing `! <command>` in the prompt; or disable "
        "the `{category}` category for this project in `~/.claude/kk-guard.json`"
    ),
    "selfmod": (
        "guard and settings files are protected from agent edits; the user "
        "edits them directly, or sets `disable_selfmod: true` for this project "
        "in `~/.claude/kk-guard.json`"
    ),
    "failure": (
        "the guard could not run ({cause}); nothing was executed; fix the "
        "guard or run the command yourself"
    ),
}


# ---------------------------------------------------------------------------
# Decision type
# ---------------------------------------------------------------------------
class Denied(Exception):
    """Raised by any check that decides the tool call must not run.

    `category` is one of secrets, destructive, selfmod, failure. `what` is
    the matched thing in the operator's words. `detail` fills the remedy
    template: the destructive category name, or the failure cause.
    """

    def __init__(self, category, what, detail=""):
        Exception.__init__(self, what)
        self.category = category
        self.what = what
        self.detail = detail

    def reason(self):
        remedy = REMEDIES[self.category]
        if self.category == "destructive":
            remedy = remedy.format(category=self.detail)
        elif self.category == "failure":
            remedy = remedy.format(cause=self.detail or "unknown error")
        return "kk guard: %s — %s. Way through: %s" % (self.category, self.what, remedy)


def failure(cause):
    return Denied("failure", "the guard could not evaluate this call", cause)


# ---------------------------------------------------------------------------
# Payload parsing
# ---------------------------------------------------------------------------
class Context(object):
    """What one hook invocation knows. `project_root` and `exec_dir` are
    distinct on purpose; see the module docstring."""

    __slots__ = ("tool_name", "tool_input", "project_root", "exec_dir", "home", "permission_mode")

    def __init__(self, tool_name, tool_input, project_root, exec_dir, home, permission_mode=""):
        self.tool_name = tool_name
        self.tool_input = tool_input
        self.project_root = project_root
        self.exec_dir = exec_dir
        self.home = home
        self.permission_mode = permission_mode


def home_dir(env):
    """Absolute home directory. A missing, empty or relative HOME would give
    the `~/` globs an anchor no absolute path can match, so fall back to the
    password database (expanduser would return `/` for an empty HOME)."""
    home = env.get("HOME")
    if home and os.path.isabs(home):
        return home
    try:
        import pwd
        home = pwd.getpwuid(os.getuid()).pw_dir
    except (ImportError, KeyError, AttributeError):
        home = os.path.expanduser("~")
    if not home or not os.path.isabs(home):
        raise failure("cannot determine an absolute home directory (HOME=%r)" % env.get("HOME"))
    return home


def parse_payload(raw, env, fallback_cwd=None):
    """Turn the raw stdin text into a Context, or raise a `failure` Denied."""
    if not raw or not raw.strip():
        raise failure("empty payload")
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise failure("payload is not valid JSON: %s" % exc)
    return context_from_payload(payload, env, fallback_cwd)


def context_from_payload(payload, env, fallback_cwd=None):
    if not isinstance(payload, dict):
        raise failure("payload is not a JSON object")
    tool_name = payload.get("tool_name")
    if not isinstance(tool_name, str) or not tool_name:
        raise failure("payload has no tool_name")
    tool_input = payload.get("tool_input")
    if tool_input is None:
        tool_input = {}
    if not isinstance(tool_input, dict):
        raise failure("tool_input is not a JSON object")

    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        cwd = fallback_cwd or os.getcwd()
    if not os.path.isabs(cwd):
        raise failure("payload cwd %r is not an absolute path" % cwd)
    exec_dir = os.path.normpath(cwd)

    project_root = env.get("KK_GUARD_PROJECT_ROOT") or env.get("CLAUDE_PROJECT_DIR") or exec_dir
    if not os.path.isabs(project_root):
        raise failure("project root %r is not an absolute path" % project_root)
    project_root = os.path.normpath(project_root)

    mode = payload.get("permission_mode")
    if not isinstance(mode, str):
        mode = ""
    return Context(tool_name, tool_input, project_root, exec_dir, home_dir(env), mode)


# ---------------------------------------------------------------------------
# Declaration loading
# ---------------------------------------------------------------------------
def default_rules_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard-rules.json")


def rules_path(env):
    return env.get("KK_GUARD_RULES") or default_rules_path()


def load_rules(path):
    """Load and validate the declaration, or raise a `failure` Denied."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            rules = json.load(handle)
    except OSError as exc:
        raise failure("cannot read rules file %s: %s" % (path, exc.strerror or exc))
    except ValueError as exc:
        raise failure("rules file %s is not valid JSON: %s" % (path, exc))
    if not isinstance(rules, dict):
        raise failure("rules file %s is not a JSON object" % path)
    version = rules.get("version")
    # `True in (1,)` and `1.0 in (1,)` both hold; require a real integer.
    if type(version) is not int or version not in SUPPORTED_VERSIONS:
        raise failure(
            "rules file %s declares version %r; this engine supports %s"
            % (path, version, ", ".join(str(v) for v in SUPPORTED_VERSIONS))
        )
    for key, kind in (("secrets", list), ("destructive", dict), ("tmp_roots", list), ("selfmod", list)):
        if not isinstance(rules.get(key), kind):
            raise failure("rules file %s: %r must be a %s" % (path, key, kind.__name__))
    if not all(isinstance(entry, str) for entry in rules["secrets"]):
        raise failure("rules file %s: every secrets entry must be a string" % path)
    return rules


# ---------------------------------------------------------------------------
# Glob matcher
# ---------------------------------------------------------------------------
def _glob_body_to_regex(body):
    """Translate the part of a permission glob after its anchor.

    `**/` is an optional run of directories, a trailing `/**` is "and
    anything beneath", `*` stays within one segment, `?` is one character.
    A trailing `/` names a directory and everything beneath it.
    """
    body = body.strip("/")
    out = []
    i = 0
    n = len(body)
    while i < n:
        ch = body[i]
        if body.startswith("**/", i):
            out.append("(?:[^/]+/)*")
            i += 3
        elif body.startswith("**", i):
            out.append(".*")
            i += 2
        elif ch == "*":
            out.append("[^/]*")
            i += 1
        elif ch == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(ch))
            i += 1
    return "".join(out)


def validate_glob(pattern):
    """Reject glob shapes whose meaning here could differ from Claude Code's.

    Accepted anchors are `//` (absolute), `~/` (home), `./` (project root)
    and an unanchored pattern (project root, gitignore semantics). A single
    leading `/` is ambiguous between the two harness layers, and gitignore
    character classes and negation are not implemented; refusing them keeps
    the hook and the settings projection from reading one glob two ways.
    """
    if not isinstance(pattern, str) or not pattern:
        raise ValueError("empty glob")
    if pattern.startswith("/") and not pattern.startswith("//"):
        raise ValueError("glob %r: use // for an absolute path or ./ for the project root" % pattern)
    if pattern.startswith("!"):
        raise ValueError("glob %r: negation is not supported" % pattern)
    if "[" in pattern or "]" in pattern:
        raise ValueError("glob %r: character classes are not supported" % pattern)
    # Paths are normalised before matching, so a `.`, `..` or empty segment
    # could never match anything; refuse it rather than silently match nothing.
    if pattern.startswith(("//", "./")):
        body = pattern[2:]
    elif pattern == "~" or pattern.startswith("~/"):   # same anchor test as glob_to_regex
        body = pattern[1:]
    else:
        body = pattern
    body = body.strip("/")
    if body:
        for segment in body.split("/"):
            if segment in ("", ".", ".."):
                raise ValueError("glob %r: empty, . and .. segments can never match a normalised path" % pattern)


def glob_to_regex(pattern, project_root, home):
    """Compile a Claude Code permission glob into a regex over absolute paths.

    Anchors: `//` absolute, `~/` home, `./` or bare relative to the project
    root. A bare name with no `/` matches its basename at any depth under the
    anchor. A pattern ending in `/**` or `/` also matches the directory
    itself, so a Grep rooted at `~/.aws` is caught by `~/.aws/**`.
    """
    validate_glob(pattern)
    bare = False
    if pattern.startswith("//"):
        anchor, body = "/", pattern[2:]
    elif pattern == "~" or pattern.startswith("~/"):
        anchor, body = home, pattern[1:]
    elif pattern.startswith("./"):
        anchor, body = project_root, pattern[2:]
    else:
        # no anchor: gitignore semantics, a single segment matches at any depth
        anchor, body = project_root, pattern
        bare = "/" not in pattern.strip("/")

    beneath = body.endswith("/**") or body.endswith("/")
    if body.endswith("/**"):
        body = body[:-3]
    body = body.strip("/")
    if bare and body:
        core = "(?:[^/]+/)*" + _glob_body_to_regex(body)
    else:
        core = _glob_body_to_regex(body)

    anchor_re = re.escape(os.path.normpath(anchor).rstrip("/"))
    if core:
        regex = "^" + anchor_re + "/" + core
    else:
        regex = "^" + anchor_re
    # DOTALL so a newline inside a filename cannot escape `**`; \Z rather than
    # `$` so a trailing newline is part of the name, not ignored.
    regex += r"(?:/.*)?\Z" if beneath else r"\Z"
    return re.compile(regex, re.DOTALL)


def anchor_forms(path):
    """The logical path and its canonical form, deduplicated.

    HOME and the project root routinely pass through symlinks (macOS `/tmp`
    and `/var/folders` live under `/private`; some hosts symlink `/home`).
    Globs are compiled against both so a call naming the physical path and
    a call naming the logical path are judged the same way.
    """
    forms = [path]
    canonical = os.path.realpath(path)
    if canonical != path:
        forms.append(canonical)
    return forms


class Policy(object):
    """The effective rules for one invocation, with globs compiled."""

    __slots__ = ("secrets", "destructive", "tmp_roots", "selfmod")

    def __init__(self, secrets, destructive, tmp_roots, selfmod):
        self.secrets = secrets          # list of (glob, compiled regex)
        self.destructive = destructive  # map category -> rules; matcher not implemented yet
        self.tmp_roots = tmp_roots
        self.selfmod = selfmod          # raw entries; check not implemented yet


def compile_policy(rules, ctx):
    """Compile the secrets globs against every anchor form (see
    `anchor_forms`). One glob yields one regex per (root, home) combination
    that differs; `secrets_match` reports the glob, not the regex."""
    secrets = []
    roots = anchor_forms(ctx.project_root)
    homes = anchor_forms(ctx.home)
    for glob in rules["secrets"]:
        try:
            for root in roots:
                for home in homes:
                    secrets.append((glob, glob_to_regex(glob, root, home)))
        except (ValueError, re.error) as exc:
            raise failure("cannot compile secrets glob %r: %s" % (glob, exc))
    return Policy(secrets, rules["destructive"], rules["tmp_roots"], rules["selfmod"])


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------
def expand_tilde(path, home):
    if path == "~":
        return home
    if path.startswith("~/"):
        return os.path.join(home, path[2:])
    return path


def resolve(path, exec_dir, home):
    """Return (requested, resolved) absolute paths for a tool argument.

    `requested` is the argument after `~` expansion, joining onto the
    execution directory and lexical normalisation; `resolved` follows
    symlinks. Deny rules apply when either matches, mirroring Claude Code.

    `realpath` runs on the un-normalised path: collapsing `..` first would
    turn `/tmp/link/../x` into `/tmp/x` before the symlink is followed, while
    the kernel resolves `link` first and lands beside the link's target.
    """
    path = expand_tilde(path, home)
    if not os.path.isabs(path):
        path = os.path.join(exec_dir, path)
    requested = os.path.normpath(path)
    resolved = os.path.realpath(path)
    return requested, resolved


def secrets_match(paths, policy):
    """The first secrets glob matching any of `paths`, or None."""
    for glob, regex in policy.secrets:
        for candidate in paths:
            if regex.match(candidate):
                return glob
    return None


# ---------------------------------------------------------------------------
# File tools
# ---------------------------------------------------------------------------
def file_tool_path(tool_name, tool_input):
    for key in PATH_KEYS.get(tool_name, ()):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def check_file_tool(tool_name, tool_input, ctx, policy):
    """Deny a file-tool call whose path is a secret. Grep and Glob with no
    search root are allowed: only the root is checked, never results."""
    path = file_tool_path(tool_name, tool_input)
    if path is None:
        if tool_name in ("Grep", "Glob"):
            return
        raise failure("%s call carries no path" % tool_name)
    requested, resolved = resolve(path, ctx.exec_dir, ctx.home)
    glob = secrets_match((requested, resolved), policy)
    if glob:
        raise Denied("secrets", "%s of %s matches %s" % (tool_name, path, glob))
    # TODO: the self-modification check for Edit, Write and NotebookEdit
    # (requested/resolved path equal to, beneath, or an ancestor of a
    # `policy.selfmod` entry) is not implemented yet; those edits are
    # currently allowed.


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
def evaluate(ctx, policy):
    """Run the checks for one call. Returns None (allow) or raises Denied."""
    if ctx.tool_name in FILE_TOOLS:
        check_file_tool(ctx.tool_name, ctx.tool_input, ctx, policy)
        return
    # TODO: Bash command analysis, apply_patch header parsing and the capy
    # execution tools are not implemented yet; those calls are currently
    # allowed. Unknown tools are allowed by design: dispatch is the engine's
    # job and the wrapper never filters by tool name.
    return


def decide(raw, env, fallback_cwd=None):
    """Full pipeline from raw stdin text to a decision (None or Denied)."""
    ctx = parse_payload(raw, env, fallback_cwd)
    rules = load_rules(rules_path(env))
    policy = compile_policy(rules, ctx)
    evaluate(ctx, policy)


# ---------------------------------------------------------------------------
# Emitter and entry point
# ---------------------------------------------------------------------------
def deny_output(reason):
    return json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    })


def emit_deny(denied, stdout=None, stderr=None):
    """Write the deny on both channels. The caller exits 2."""
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    reason = denied.reason()
    stdout.write(deny_output(reason) + "\n")
    stdout.flush()
    stderr.write(reason + "\n")
    stderr.flush()


def main():
    raw = sys.stdin.buffer.read().decode("utf-8", "replace")
    try:
        decide(raw, os.environ)
    except Denied as denied:
        emit_deny(denied)
        return 2
    except Exception as exc:  # fail closed on anything unexpected
        emit_deny(failure("%s: %s" % (type(exc).__name__, exc)))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
