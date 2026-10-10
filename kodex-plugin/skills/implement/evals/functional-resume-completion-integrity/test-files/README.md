# Label reader

Python 3.9+, standard library only. Run `python3 -B -m unittest discover -s tests`.
The public list_labels API reads rows supplied by its caller.
state/records.json and state/release.json contain the checked-in synthetic
compatibility snapshot. They are local source evidence, not live production access.
