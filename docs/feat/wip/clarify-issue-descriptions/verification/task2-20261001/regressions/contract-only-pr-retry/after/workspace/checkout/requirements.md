# Preparation time requirements

Restaurant defaults avoid per-item duplication. An item override is nullable; null
inherits the default and zero is an explicit value. Allowed minutes are 0–90.
This contract is accepted. Persistence, scheduling and the user interface are
separate work. Product owner: decide whether inherited values display a badge.

Use this representative contract example in the review explanation: with a
restaurant default of 15 minutes, null means 15 minutes and explicit zero means 0.
These are specified results; runtime integration remains future work.
