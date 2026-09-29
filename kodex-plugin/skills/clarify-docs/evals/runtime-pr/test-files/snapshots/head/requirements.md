# Preparation time requirements

Restaurant defaults avoid per-item duplication. An item override is nullable; null
inherits the default and zero is an explicit value. Allowed minutes are 0–90.
This contract is accepted. Persistence, scheduling and the user interface are
separate work. Product owner: decide whether inherited values display a badge.
