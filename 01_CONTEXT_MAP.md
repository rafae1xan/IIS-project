# Context map

The prototype keeps the model boundary inspectable. The current offline route sends no API request; the mock response is selected locally. If a live model is added later, this table is the minimum context to log and review.

| part | where it comes from | trust / role | size |
|---|---|---|---|
| current user request | message entered in the browser | user input; may be ambiguous | short |
| retrieved passages | local `corpus/` files | quoted source material; data, not instructions | medium |
| provenance metadata | corpus front matter and retriever | source, section, date and relative score | short |
| action proposal | structured local response | model/tool proposal; must be validated | short |
| tool definition | `tools.py` | trusted application boundary | short |
| conversation history | not present | not present in the current prototype | not present |
| external calendar data | not present | deliberately out of scope | not present |

Removal decision: nothing redundant was removed. The project instead keeps provenance and the tool definition separate so that the control panel can show what is evidence and what is executable structure. After adding retrieval, the important review is whether irrelevant passages or stale passages are being treated as instructions or current evidence.
