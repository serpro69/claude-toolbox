# Batch report

Python 3.9+, standard library only. Run `python3 -B -m unittest discover -s tests`.

`report(values, detailed=None)` accepts a finite list of numbers. Omitting the
mode uses the checked-in DETAILED_REPORT setting; an explicit Boolean overrides
that default for the call. Plain reports contain `Items: N`. Detailed reports
for populated batches append `; Mean: M`, formatting the arithmetic mean with
Python's `g` format. Empty batches are valid in either mode and produce only
`Items: 0`; there is no mean to display.

This increment enables the existing detailed output by default. Preserve explicit
plain/detailed overrides, counts, and successful empty-batch reports. Historical
installation settings are not recorded here. Review the staged increment against
this contract; no live deployment operation is requested.
