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

Tokenizer helpers and wrapper tables are adapted from safe-claude-code,
Copyright 2026 - present; serpro69, Elastic License 2.0 (ELv2). Modified
here to preserve operand boundaries and executable bodies, handle heredocs,
and use Claude Code's separator set. License terms accompany this plugin
in LICENSE.md beside this file. Parsing is static: commands and interpreter
code are never run.
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
        self.selfmod = selfmod          # list of (entry, absolute protected path)


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
    selfmod = []
    for entry in rules["selfmod"]:
        if not isinstance(entry, str) or not entry:
            raise failure("every selfmod entry must be a nonempty path")
        base = entry[:-3] if entry.endswith("/**") else entry
        if any(ch in base for ch in "*?[]"):
            raise failure("selfmod paths support only a trailing /**: %r" % entry)
        if base.startswith("//"):
            base = base[1:]
        selfmod.extend((entry, path) for path in resolve(base, ctx.project_root, ctx.home))
    return Policy(secrets, rules["destructive"], rules["tmp_roots"], selfmod)


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


def selfmod_match(paths, policy):
    """Protect both sides of a directory move, with path-component boundaries."""
    for entry, protected in policy.selfmod:
        for path in paths:
            if (path == protected or path.startswith(protected.rstrip("/") + "/")
                    or protected.startswith(path.rstrip("/") + "/")):
                return entry
    return None


def check_path(path, ctx, policy, action, mutation=False):
    paths = resolve(path, ctx.exec_dir, ctx.home)
    glob = secrets_match(paths, policy)
    if glob:
        raise Denied("secrets", "%s of %s matches %s" % (action, path, glob))
    entry = selfmod_match(paths, policy) if mutation else None
    if entry:
        raise Denied("selfmod", "%s of %s affects %s" % (action, path, entry))


# ---------------------------------------------------------------------------
# Shell structure. Keep raw spelling and decoded operands separate from prose.
# ---------------------------------------------------------------------------
QUOTED = re.compile(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
SEPARATORS = {"&&", "||", ";", "|", "|&", "&", "\n"}
CHAIN_SEPARATORS = SEPARATORS - {"|", "|&"}
REDIRECTIONS = {">", ">>", ">|", "&>", "&>>", "<", "<>", ">&", "<&", "<<", "<<-", "<<<"}
SHELL_OPERATORS = sorted(SEPARATORS | REDIRECTIONS | {"(", ")"}, key=len, reverse=True)
WRAPPERS = {
    "env", "nohup", "time", "nice", "ionice", "caffeinate", "stdbuf", "command",
    "builtin", "exec", "xargs", "noglob", "nocorrect", "setsid", "flock", "watch",
    "timeout", "then", "do", "else", "elif", "if", "while", "until", "busybox",
    "toybox", "sudo",
}
WRAPPER_OPTIONS_WITH_ARG = {
    "timeout": {"-s", "--signal", "-k", "--kill-after"},
    "nice": {"-n", "--adjustment"},
    "ionice": {"-c", "--class", "-n", "--classdata", "-p", "--pid"},
    "env": {"-u", "--unset", "-C", "--chdir", "-S", "--split-string"},
    "xargs": {"-I", "-i", "-n", "-P", "-d", "-a", "-L", "-s", "-E", "--max-args",
              "--max-procs", "--delimiter", "--arg-file", "--max-lines", "--max-chars",
              "--eof", "--replace"},
    "watch": {"-n", "--interval"},
    "flock": {"-w", "--timeout", "-E", "--conflict-exit-code"},
    "stdbuf": {"-i", "-o", "-e", "--input", "--output", "--error"},
    "caffeinate": {"-t", "-w"},
    "sudo": {"-u", "--user", "-g", "--group", "-h", "--host", "-p", "--prompt", "-C", "-T"},
}
WRAPPER_POSITIONAL = {"timeout": 1, "flock": 1}
SHELLS = {"sh", "bash", "zsh", "ksh", "dash", "ash", "fish", "csh", "tcsh"}
INTERPRETERS = {"python", "python2", "python3", "pythonw", "perl", "ruby", "node",
                "deno", "bun", "osascript", "rscript", "r", "php", "lua", "julia"}
DATA_SINKS = {"cat", "tee", "printf"}
MAX_SHELL_DEPTH = 32


def defang(text):
    """Mask multiword quoted prose; retain single words and glued quotes."""
    text = text.replace("\\", "")
    out, i = [], 0
    for match in QUOTED.finditer(text):
        before = text[match.start() - 1] if match.start() else " "
        after = text[match.end()] if match.end() < len(text) else " "
        inner = match.group()[1:-1]
        glued = not before.isspace() or not after.isspace()
        out.extend((text[i:match.start()], inner if glued or not any(c.isspace() for c in inner) else "Q"))
        i = match.end()
    return "".join(out) + text[i:]


def strip_quotes(text):
    """Decode one shell word without splitting a quoted path at its spaces."""
    tokens, _, _ = _shell_scan(text)
    return " ".join(token.value for token in tokens)


def basename(token):
    return token.rsplit("/", 1)[-1]


def is_interpreter(program):
    return program in INTERPRETERS or re.fullmatch(r"python[23](?:\.\d+)?", program) is not None


def program_index(words):
    """Skip assignments, control words and wrappers, including option values."""
    i = 0
    while i < len(words):
        word = words[i]
        if ASSIGNMENT.match(word) or word in ("!", "{", "}"):
            i += 1
            continue
        program = basename(word)
        if program not in WRAPPERS:
            return i
        i += 1
        takes_arg = WRAPPER_OPTIONS_WITH_ARG.get(program, set())
        while i < len(words) and words[i].startswith("-") and words[i] != "-":
            option = words[i]
            i += 1
            if option == "--":
                break
            if option in takes_arg:
                i += 1
        i += WRAPPER_POSITIONAL.get(program, 0)
    return None


class ShellToken(object):
    __slots__ = ("value", "raw", "operator")

    def __init__(self, value, raw, operator=False):
        self.value, self.raw, self.operator = value, raw, operator


class ShellBody(object):
    __slots__ = ("text", "interpreter")

    def __init__(self, text, interpreter=False):
        self.text, self.interpreter = text, interpreter


def split_segments(tokens, separators=SEPARATORS):
    segment = []
    for token in tokens:
        if token.operator and token.value in separators:
            if segment:
                yield segment
            segment = []
        else:
            segment.append(token)
    if segment:
        yield segment


def command_words(tokens):
    """Remove redirections, their targets and adjacent numeric descriptors."""
    words = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.operator and token.value in REDIRECTIONS:
            i += 2
            continue
        if not token.operator:
            words.append(token.value)
        i += 1
    return words


def command_position_tokens(text):
    tokens, _, _ = _shell_scan(text)
    for segment in split_segments(tokens):
        words = command_words(segment)
        index = program_index(words)
        if index is not None:
            yield basename(words[index])


def _heredoc_consumer(tokens, position):
    # Inspect the whole pipeline: `cat <<EOF | ./import.sh` feeds executable
    # or unknown input even though the first process is a known data sink.
    start = position
    while start and not (tokens[start - 1].operator and tokens[start - 1].value in CHAIN_SEPARATORS):
        start -= 1
    end = position
    while end < len(tokens) and not (tokens[end].operator and tokens[end].value in CHAIN_SEPARATORS):
        end += 1
    programs = []
    for segment in split_segments(tokens[start:end]):
        words = command_words(segment)
        index = program_index(words)
        if index is not None:
            programs.append(basename(words[index]))
    for program in programs:
        if program not in DATA_SINKS:
            return program
    return "cat"  # all data sinks, or a redirection without a command


def _substitution(text, i, depth):
    """Read one executable body; the recursive lexer respects heredoc spans."""
    if text.startswith(("$(", "<(", ">("), i):
        _, _, end = _shell_scan(text, i + 2, ")", depth + 1)
        return ShellBody(text[i + 2:end]), end + 1
    if text[i] == "`":
        j = i + 1
        while j < len(text):
            if text[j] == "\\":
                j += 2
            elif text[j] == "`":
                return ShellBody(text[i + 1:j]), j + 1
            else:
                j += 1
        raise failure("unterminated backtick substitution")
    return None, i


def _heredoc_substitutions(text, depth):
    # Quotes in an expandable heredoc are data, not shell quote delimiters.
    bodies, i = [], 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text) and text[i + 1] in "\\$`\n":
            i += 2
            continue
        if text.startswith("$(", i) or text[i] == "`":
            body, i = _substitution(text, i, depth)
            bodies.append(body)
        else:
            i += 1
    return bodies


def _ansi_escape(text, i):
    """Decode an escape inside Bash's $'...' without evaluating shell text."""
    char = text[i + 1]
    simple = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f",
              "n": "\n", "r": "\r", "t": "\t", "v": "\v", "\\": "\\", "'": "'", '"': '"'}
    if char in simple:
        return simple[char], i + 2
    if char == "c" and i + 2 < len(text):
        return chr(ord(text[i + 2].upper()) & 31), i + 3
    if char in "01234567":
        match = re.match(r"[0-7]{1,3}", text[i + 1:])
        return chr(int(match.group(), 8) % 256), i + 1 + len(match.group())
    if char in "xuU":
        width = {"x": 2, "u": 4, "U": 8}[char]
        match = re.match(r"[0-9a-fA-F]{1,%d}" % width, text[i + 2:])
        if match:
            return chr(int(match.group(), 16)), i + 2 + len(match.group())
    return "\\" + char, i + 2


def _shell_scan(text, start=0, stop="", depth=0):
    """Quote-aware lexer; consume heredocs before interpreting their contents.

    Returns (tokens, executable bodies, end offset). Substitution output is
    represented by Q in operand words; its original code is inspected through
    a separate body. This prevents literal heredoc prose becoming operands.
    """
    if depth > MAX_SHELL_DEPTH:
        raise failure("shell nesting exceeds the inspection limit")
    tokens, bodies, pending = [], [], []
    i, group_depth = start, 0
    while i < len(text):
        ch = text[i]
        if stop and ch == stop and group_depth == 0:
            return tokens, bodies, i
        if ch in " \t":
            i += 1
            continue
        if ch == "#":
            end = text.find("\n", i)
            i = len(text) if end < 0 else end
            continue
        operator = next((op for op in SHELL_OPERATORS if text.startswith(op, i)), None)
        if text.startswith(("$(", "<(", ">("), i):
            operator = None
        if operator:
            if operator == "(":
                group_depth += 1
            elif operator == ")":
                group_depth -= 1
            # An unquoted descriptor glued to a redirect is syntax, not a file.
            if operator in REDIRECTIONS and tokens and tokens[-1].raw.isdigit() and i > start and text[i - 1].isdigit():
                tokens.pop()
            tokens.append(ShellToken(operator, operator, True))
            i += len(operator)
            if operator == "\n":
                for position, delimiter, quoted, tabs in pending:
                    lines = []
                    while i < len(text):
                        end = text.find("\n", i)
                        end = len(text) if end < 0 else end
                        line = text[i:end]
                        i = min(end + 1, len(text))
                        line = line.lstrip("\t") if tabs else line
                        if line == delimiter:
                            break
                        lines.append(line + ("\n" if end < len(text) else ""))
                    else:
                        raise failure("unterminated heredoc")
                    body = "".join(lines)
                    consumer = _heredoc_consumer(tokens, position)
                    if not quoted:
                        bodies.extend(_heredoc_substitutions(body, depth))
                    if consumer not in DATA_SINKS:
                        bodies.append(ShellBody(body, is_interpreter(consumer)))
                pending = []
            continue
        begin, quote, value = i, "", []
        while i < len(text):
            ch = text[i]
            if not quote and text.startswith(("$'", '$"'), i):
                quote = "$'" if text[i + 1] == "'" else '"'
                i += 2
                continue
            if ch == "\\" and quote != "'":
                if i + 1 >= len(text):
                    raise failure("unterminated shell escape")
                if quote == "$'":
                    decoded, i = _ansi_escape(text, i)
                    value.append(decoded)
                    continue
                following = text[i + 1]
                if quote == '"' and following not in '$`"\\\n':
                    value.append("\\")
                    i += 1
                else:
                    if following != "\n":
                        value.append(following)
                    i += 2
                continue
            if ch in "'\"" and (not quote or ch == quote or (quote == "$'" and ch == "'")):
                quote = "" if quote else ch
                i += 1
                continue
            expandable = quote not in ("'", "$'") and (text.startswith("$(", i) or ch == "`" or
                                           (not quote and text.startswith(("<(", ">("), i)))
            if expandable:
                body, i = _substitution(text, i, depth)
                bodies.append(body)
                value.append("Q")
                continue
            if not quote and (ch in " \t\n" or any(text.startswith(op, i) for op in SHELL_OPERATORS)):
                break
            value.append(ch)
            i += 1
        if quote:
            raise failure("unterminated shell quote")
        token = ShellToken("".join(value), text[begin:i])
        if tokens and tokens[-1].operator and tokens[-1].value in ("<<", "<<-"):
            pending.append((len(tokens) - 1, token.value, any(c in token.raw for c in "'\"\\"), tokens[-1].value == "<<-"))
        tokens.append(token)
    if stop or pending:
        raise failure("unterminated shell substitution or heredoc")
    return tokens, bodies, i


def short_option_argument(word, name, value_options):
    """Find a short flag in a cluster, stopping at options which consume text."""
    if not word.startswith("-") or word.startswith("--"):
        return None
    for i, char in enumerate(word[1:], 1):
        if char == name:
            return word[i + 1:]
        if char in value_options:
            break
    return None


def inline_code(words, shell=False):
    """Return the argument of a shell -c or interpreter -c/-e invocation."""
    index = program_index(words)
    if index is None:
        return None
    program = basename(words[index])
    eligible = program in SHELLS if shell else is_interpreter(program)
    if not eligible:
        return None
    flags = {"-c"} if shell else {"-c", "-e", "--eval", "-p", "--print"}
    for i in range(index + 1, len(words)):
        word = words[i]
        if word in flags or (shell and re.fullmatch(r"-[a-zA-Z]*c[a-zA-Z]*", word)):
            if i + 1 >= len(words):
                raise failure("inline interpreter option has no code argument")
            return words[i + 1]
        if not shell and (word.startswith("--eval=") or word.startswith("--print=")):
            return word.split("=", 1)[1]
        if not shell:
            option = "c" if program.startswith("python") else "e"
            attached = short_option_argument(word, option, "cWX" if option == "c" else "ep")
            if attached is not None:
                if attached:
                    return attached
                if i + 1 >= len(words):
                    raise failure("inline interpreter option has no code argument")
                return words[i + 1]
        if not word.startswith("-"):
            break
    return None


def extract_bodies(text):
    """Original executable text, before defang; heredoc literals stay opaque."""
    tokens, bodies, _ = _shell_scan(text)
    for segment in split_segments(tokens):
        code = inline_code(command_words(segment), shell=True)
        if code is not None:
            bodies.append(ShellBody(code))
    return bodies


def substitution_bodies(text):
    return [body.text for body in _shell_scan(text)[1]]


def path_like(word, ctx):
    return bool(word) and ("/" in word or word.startswith(("~", ".")) or
                           os.path.exists(os.path.join(ctx.exec_dir, word)))


def mutation_operands(segment, words):
    """Literal write targets; reads of settings remain permitted."""
    targets = []
    for i, token in enumerate(segment[:-1]):
        if token.operator and token.value in {">", ">>", ">|", "&>", "&>>", "<>", ">&"}:
            target = segment[i + 1].value
            if not (token.value == ">&" and (target.isdigit() or target == "-")):
                targets.append(target)
    index = program_index(words)
    if index is None:
        return targets
    program, args = basename(words[index]), words[index + 1:]
    operands, target_dir = [], None
    options = True
    i = 0
    while i < len(args):
        arg = args[i]
        if options and arg == "--":
            options = False
        elif options and program in {"cp", "mv", "install", "ln"} and arg in {"-t", "--target-directory"}:
            if i + 1 < len(args):
                target_dir = args[i + 1]
                i += 1
        elif options and program in {"cp", "mv", "install", "ln"} and arg.startswith("--target-directory="):
            target_dir = arg.split("=", 1)[1]
        elif options and program in {"cp", "mv", "install", "ln"} and short_option_argument(arg, "t", "tSmog") is not None:
            target_dir = short_option_argument(arg, "t", "tSmog")
            if not target_dir and i + 1 < len(args):
                i += 1
                target_dir = args[i]
        elif options and program == "sed" and arg in {"-e", "--expression", "-f", "--file"}:
            i += 1
        elif options and program == "sed" and short_option_argument(arg, "i", "efi") == "":
            # BSD sed consumes a separate backup suffix; the common empty
            # suffix is not a filename (resolving it would mean project root).
            if i + 1 < len(args) and args[i + 1] == "":
                i += 1
        elif not options or not arg.startswith("-") or arg == "-":
            operands.append(arg)
        i += 1
    if program == "tee":
        targets.extend(operands)
    elif program == "sed" and any(a == "--in-place" or a.startswith("--in-place=") or
                                 short_option_argument(a, "i", "efi") is not None for a in args):
        # Including the script is conservative; it cannot hide the file operands.
        targets.extend(operands)
    elif program == "dd":
        targets.extend(a[3:] for a in args if a.startswith("of="))
    elif program == "mv":
        targets.extend(operands)
    elif program in {"cp", "install", "ln"} and operands:
        targets.append(target_dir or operands[-1])
        if program == "ln" and any(a == "--force" or re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*", a) for a in args):
            targets.extend(operands)
    if target_dir:
        targets.append(target_dir)
    return targets


# Literal-only interpreter inspection: never eval the source or expand paths.
CODE_STRING = re.compile(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"", re.DOTALL)
WRITE_CALL = re.compile(r"\b(open|(?:shutil\.)?(?:copy\w*|move)|os\.(?:rename|replace|remove|unlink)|"
                        r"(?:fs\.)?(?:writeFile\w*|appendFile\w*|rename\w*|rm\w*|unlink\w*))\s*\(")
PATH_WRITE = re.compile(r"\b(?:pathlib\.)?Path\s*\(\s*(?P<path>'[^']*'|\"[^\"]*\")\s*\)"
                        r"\s*\.write_\w*\s*\(")


def call_arguments(text, start):
    """Split literal call arguments at top-level commas without executing code."""
    args, begin, i, nesting, quote = [], start, start, 0, ""
    while i < len(text):
        char = text[i]
        if quote:
            if char == "\\":
                i += 2
                continue
            if char == quote:
                quote = ""
        elif char in "'\"`":
            quote = char
        elif char in "([{":
            nesting += 1
        elif char == ")" and not nesting:
            return args + [text[begin:i].strip()]
        elif char in ")]}":
            nesting -= 1
        elif char == "," and not nesting:
            args.append(text[begin:i].strip())
            begin = i + 1
        i += 1
    return args + [text[begin:].strip()]


def literal_argument(argument):
    argument = re.sub(r"^[A-Za-z_]\w*\s*=\s*", "", argument)
    match = CODE_STRING.fullmatch(argument)
    return next((s for s in match.groups() if s is not None), None) if match else None


def named_argument(args, name, position, default=None):
    for arg in args:
        if re.match(re.escape(name) + r"\s*=", arg):
            return arg.split("=", 1)[1].strip()
    positional = [arg for arg in args if not re.match(r"[A-Za-z_]\w*\s*=", arg)]
    return positional[position] if len(positional) > position else default


def check_inline_code(code, ctx, policy):
    for match in CODE_STRING.finditer(code):
        path = next(s for s in match.groups() if s is not None)
        if path_like(path, ctx):
            check_path(path, ctx, policy, "inline code")
    for match in WRITE_CALL.finditer(code):
        name, args = match.group(1), call_arguments(code, match.end())
        if name == "open":
            mode = literal_argument(named_argument(args, "mode", 1, "'r'"))
            selected = [named_argument(args, "file", 0)] if mode is not None and any(c in mode for c in "wax+") else []
        elif "copy" in name:
            selected = [named_argument(args, "dst", 1)]
        elif name in {"move", "shutil.move", "os.rename", "os.replace"} or "rename" in name:
            selected = [named_argument(args, "src", 0), named_argument(args, "dst", 1)]
        else:
            selected = [named_argument(args, "path", 0)]
        for argument in selected:
            if argument is None:
                continue
            path = literal_argument(argument)
            if path is not None:
                check_path(path, ctx, policy, "inline write", mutation=True)
    for match in PATH_WRITE.finditer(code):
        check_path(literal_argument(match.group("path")), ctx, policy, "inline write", mutation=True)


def check_command(command, ctx, policy, depth=0):
    if depth > MAX_SHELL_DEPTH:
        raise failure("shell nesting exceeds the inspection limit")
    tokens, bodies, _ = _shell_scan(command)
    for segment in split_segments(tokens):
        words = command_words(segment)
        shell_code = inline_code(words, shell=True)
        code = inline_code(words)
        if shell_code is not None:
            bodies.append(ShellBody(shell_code))
        if code is not None:
            check_inline_code(code, ctx, policy)
        index = program_index(words)
        program = basename(words[index]) if index is not None else ""
        for i, token in enumerate(segment[:-1]):
            if token.operator and token.value == "<<<":
                text = segment[i + 1].value
                consumer = _heredoc_consumer(tokens, tokens.index(token))
                if is_interpreter(consumer):
                    check_inline_code(text, ctx, policy)
                elif consumer not in DATA_SINKS:
                    bodies.append(ShellBody(text))
        if program == "dd":
            for arg in words[index + 1:]:
                if arg.startswith(("if=", "of=")):
                    check_path(arg[3:], ctx, policy, "Bash")
        # Prose matching belongs to the destructive tier; path checks always
        # use these intact operands, never defang's lossy representation.
        for word in words:
            if word != code and word != shell_code and path_like(word, ctx):
                check_path(word, ctx, policy, "Bash")
        for i, token in enumerate(segment[:-1]):
            if token.operator and token.value in REDIRECTIONS - {"<<", "<<-", "<<<", ">&", "<&"}:
                check_path(segment[i + 1].value, ctx, policy, "Bash redirection")
        for path in mutation_operands(segment, words):
            check_path(path, ctx, policy, "Bash write", mutation=True)
    for body in bodies:
        if body.interpreter:
            check_inline_code(body.text, ctx, policy)
        else:
            check_command(body.text, ctx, policy, depth + 1)


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
    check_path(path, ctx, policy, tool_name, mutation=tool_name in ("Edit", "Write", "NotebookEdit"))


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
def evaluate(ctx, policy):
    """Run the checks for one call. Returns None (allow) or raises Denied."""
    if ctx.tool_name in FILE_TOOLS:
        check_file_tool(ctx.tool_name, ctx.tool_input, ctx, policy)
        return
    if ctx.tool_name == "Bash":
        command = ctx.tool_input.get("command")
        if not isinstance(command, str):
            raise failure("Bash command must be a string")
        check_command(command, ctx, policy)
        return
    # TODO: apply_patch header parsing and the capy
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
