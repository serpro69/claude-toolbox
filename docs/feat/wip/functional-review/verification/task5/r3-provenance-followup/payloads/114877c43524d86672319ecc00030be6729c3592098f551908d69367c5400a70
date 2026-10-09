[CRITICAL] client.py:5 – Backward Incompatibility with Released Provider
The unconditional check `if response.get("applied") is not True:` violates the delivery contract. The released provider at `eval-release` returns `{"ok": True}` without an `applied` key. Because this check is not gated by the `enhanced_settings` flag, ordinary saves (where `enhanced_settings=False`) now raise a `RuntimeError` even though the legacy provider successfully persisted the data. This creates a data integrity mismatch where the caller sees a failure but the state was mutated.
→ Fix: Gate the receipt validation so it is only enforced when `enhanced_settings` is requested.
```python
    if not response.get("ok"):
        raise RuntimeError("Settings save failed")
    # Only strictly require the receipt if enhanced settings are enabled
    if enhanced_settings and response.get("applied") is not True:
        raise RuntimeError("Provider did not acknowledge applied settings")
    return {"saved": True, "enhanced": enhanced_settings}
```

[HIGH] tests/test_client.py:7 – Unit test masks baseline compatibility regression
The mock `send` function was updated to return `{"ok": True, "applied": True}` unconditionally. This encodes the behavior of the pending Task 2 provider rather than the released `eval-release` baseline. Because the test no longer exercises the legacy response payload, it allowed a critical compatibility regression to pass locally.
→ Fix: Revert the primary test to assert compatibility with the legacy provider baseline, and add a separate test for the enhanced/receipt flow.
```python
    def test_ordinary_save_legacy_provider(self):
        def send_legacy(workspace, request):
            return {"ok": True}  # Legacy eval-release provider
        self.assertEqual(save_settings(send_legacy, "w", {"label": "blue"}),
                         {"saved": True, "enhanced": False})

    def test_enhanced_save_with_receipt(self):
        def send_enhanced(workspace, request):
            return {"ok": True, "applied": True}
        self.assertEqual(save_settings(send_enhanced, "w", {"label": "blue"}, enhanced_settings=True),
                         {"saved": True, "enhanced": True})
```

• **Overall Code Quality Summary:** 
The proposed increment accurately attempts to fulfill Task 1 by implementing receipt handling on the client. However, it fails to fulfill the explicit architectural constraint of independent releasability. By forcefully changing the contract to expect a receipt on *all* saves, the client immediately breaks backwards compatibility with the current `eval-release` provider. The unit test updates contributed to this blindspot by completely overwriting the legacy contract instead of verifying both the legacy and enhanced execution paths.

• **Top 3 Priority Fixes:**
1. Update `client.py` to condition the `response.get("applied")` receipt check on `enhanced_settings` being `True`.
2. Add a unit test specifically verifying that `save_settings(..., enhanced_settings=False)` succeeds when the provider only returns `{"ok": True}`.
3. Add a separate unit test verifying that an enhanced save correctly processes the new `{"ok": True, "applied": True}` receipt.

• **Positive Aspects:**
- The client-side telemetry payload update (`{"require_receipt": True}`) is implemented safely; it transmits the new requirement without causing server-side faults, as the legacy provider cleanly ignores unknown keys in the request dictionary.
- The use of `is not True` appropriately handles potential `None` or missing values cleanly without throwing `AttributeError` or `KeyError`.
