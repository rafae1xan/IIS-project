# Demonstration walkthrough

Run `python app.py`, then open the printed local address.

1. Select **Ask with evidence**. The right panel shows the answer, quoted passage, source, section, date and score.
2. Select **Test stale source**. The old handbook is labelled `SUPERSEDED`; the newer passage is used for the answer.
3. Select **Propose an action**. Inspect the selected object, 90-minute parameter, impact, uncertainty and reversibility. Nothing has changed yet.
4. Select **Cancel** to demonstrate recovery without a file change, then repeat and select **Confirm**. The tool result and log entry are shown.
5. Run `python tools.py --selftest` to demonstrate that a 900-minute call is refused before execution.
6. Select the two image buttons to show a confidence-bearing answer and a refusal with a reason.

All data is local and synthetic. No external calendar, API key or personal image is used.
