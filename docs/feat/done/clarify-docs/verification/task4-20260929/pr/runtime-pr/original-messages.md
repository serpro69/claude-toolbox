## commentary

I’ll read the supplied document and answer the five questions with citations, stating where the text leaves an answer unclear.


## final_answer

1. **Why does this work exist?** The document does not explain the underlying problem or intended benefit. “Schema-only stack” names the scope but provides no rationale (heading, line 1).

2. **What happens in a representative case?** No concrete case is described. The text says routing proceeds “from the sentinel to the default,” but neither term nor the resulting behavior is defined (lines 3–4).

3. **What changes in the current increment?** It adds nullable `prep_minutes`, describes “zero and 0–90 in the union,” and completes a stack step through sentinel-to-default routing. It reports three passing assertions without identifying them (lines 3–4).

4. **What remains outside it?** Persistence, scheduling, and UI “remain elsewhere.” Their status and relationship to this increment are unspecified (lines 5–6).

5. **What still needs a decision?** The product owner must choose badges; the available choices and decision criteria are missing (lines 5–6).
