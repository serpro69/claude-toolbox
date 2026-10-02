# Dense-source clean-shell retry

The initial run is retained in `../dense-source/`. Its unchanged assertions passed;
the initial grader withheld a strict boundary-compliance pass because login-shell
startup attempted a denied write to a navi log outside the manifest. The trace does
not establish successful outside-scope mutation or oracle leakage.

To remove this environmental ambiguity, fresh editor, original reader and revised
reader sessions use `login:false` for every shell command. The exact scenario
prompt, fixture content, frozen instructions, oracle, assertions, fixed questions,
model and reasoning settings remain unchanged. Each prompt records the neutral
shell setting before dispatch. No expected answers are added.
