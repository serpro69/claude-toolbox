# Batch report

Python 3.9+, standard library only. Run `python3 -B -m unittest discover -s tests`.

`report(values, detailed=None)` accepts a finite list of numbers. Omitting the
mode uses the checked-in DETAILED_REPORT setting; an explicit Boolean overrides
that default for the call. Plain reports contain the count, including zero for
an empty batch. Detailed reports for populated batches also append `; Mean: M`,
formatting the arithmetic mean with Python's `g` format.

This increment changes the count label from Items to Records. Preserve counts,
calculations, mode selection and the mean suffix. Detailed reporting is an
existing optional path; it is not being activated or redesigned in this increment.
Historical installation settings are not recorded here. Review the staged
increment; no live deployment operation is requested.
