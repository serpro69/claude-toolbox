1. Record the preparation-time override contract so items can inherit restaurant defaults without repeating the same value.
2. With a 15-minute default, `null` means 15 minutes and explicit `0` means 0 minutes. These are specified future results; runtime resolution is not implemented.
3. Only `contract.json` changes, defining `prep_minutes` as an integer from 0–90 inclusive or `null`, with explicit inheritance and zero semantics.
4. Runtime integration, persistence, scheduling and UI remain future work. `effective_minutes` still raises `NotImplementedError`.
5. The product owner must decide whether inherited values display a badge.
