# Workspace preferences

Python 3.9+, standard library only. Run `python3 -B -m unittest discover -s tests`.
The HTTP patch handler and command-line note action share settings.patch_settings.
Callers own their input dictionaries. A patch contains only explicitly supplied
keys. The optional note accepts text or None; the enabled flag is boolean.
