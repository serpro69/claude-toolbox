1. Restaurant defaults avoid repeating preparation times on every item; this PR records the accepted override contract.
2. With a 15-minute default, `null` specifies 15 minutes and explicit `0` specifies 0 minutes. These are contract results; runtime integration is future work.
3. Only `contract.json` changes, replacing an empty object with the contract: `null` or an integer from 0 to 90 inclusive.
4. Runtime integration, persistence, scheduling and UI remain outside scope. The resolver still raises `NotImplementedError`; validation covered JSON parsing only.
5. The product owner must decide whether inherited values display a badge.
