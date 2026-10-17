# Preference reads

Python 3.9+, standard library only. Run `python3 -B -m unittest discover -s tests`.

This change accepts preference IDs with surrounding whitespace. Trim the ID
before looking it up; preserve the existing resilient-read contract. A logical
read may make up to three attempts on `TransientRead`, returning the first
successful result. Exhausted transient errors propagate. `MissingPreference`
is permanent and must propagate on the first attempt. Reads have no side effects.

`Preferences.read` is the public entry point. `Repository.read_resilient`
owns the bounded retry policy; `read_once` performs one attempt. The scripted
backend models finite outcomes without sleeping, services or concurrency.
