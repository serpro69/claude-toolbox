# Settings client

Python 3.9+, standard library only. Tests: `python3 -B -m unittest discover -s tests`.
The client and provider ship independently. Every merged client increment must
support the released provider at Git tag `eval-release`, including ordinary
settings saves while enhanced_settings is false. `provider/settings.py` at that
tag is the supported provider source. Provider sources moved out of this
checkout after that release; local Git retains the release snapshot.
A successful settings save means values were applied and the caller sees success.
The candidate provider is not deployed and a pending provider task cannot change
the supported baseline. No live environment is available or required here.
