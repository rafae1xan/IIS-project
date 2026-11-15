# Lab 4 integration steps

Use this guide after the three starter self-tests pass. It shows how to connect the Lab 4 support
files to a running prototype. If you have a working Lab 3 project, keep its `app.py`, `model.py` and
`index.html`; add the Lab 4 support files beside them. If you do not have a working app, use the
`app.py`, `model.py` and `index.html` included in this Lab 4 pack as the starting prototype. Work in
one project folder and do not mix files from different copies.

The examples use the names in the supplied Lab 4 prototype. If you have a working Lab 3 app and its
names differ, connect the same three results to the matching places in your app: evidence beside an
answer, a tool confirmation before a tool runs, and an image result in the browser. If you cannot find
the matching place, use the included Lab 4 prototype and continue there.

## 1. Add the Lab 4 modules to `app.py`

Add these imports beside the existing `import model` line. If `os` or `json` is not already imported,
add those imports too:

```python
import retrieve
import tools
import vlm
import os
import json
```

If your app already has a line defining `HERE`, keep it. If it does not, add this near the other
top-level variables:

```python
HERE = os.path.dirname(os.path.abspath(__file__))
```

Add this variable near the other top-level variables:

```python
PENDING_TOOL = None
```

Keep the existing `log_context(parts)` helper and named `parts` list from Phase 1. In `turn(message)`,
add the following cases before the existing message-specific cases. They give the browser three
visible tests without requiring a network or API key:

```python
global PENDING_TOOL
if message == "__poster__":
    image = vlm.ask(os.path.join(HERE, "sample_images", "sample_poster.png"),
                    "what deadline is shown?")
    return {"reply": vlm.render(image), "options": [], "action": None,
            "unsupported_claims": [], "image": image}

if message == "__noticeboard__":
    image = vlm.ask(os.path.join(HERE, "sample_images", "sample_noticeboard.png"),
                    "what deadline is shown?")
    return {"reply": vlm.render(image), "options": [], "action": None,
            "unsupported_claims": [], "image": image}

if message == "__confirm_tool__" and PENDING_TOOL:
    result = tools.run(PENDING_TOOL)
    PENDING_TOOL = None
    return {"reply": "Tool result: " + json.dumps(result), "options": [],
            "action": None, "unsupported_claims": [], "tool_result": result}

if message == "__cancel_tool__":
    PENDING_TOOL = None
    return {"reply": "Cancelled. Nothing was added.", "options": [],
            "action": None, "unsupported_claims": []}

if "revision slot" in (message or "").lower():
    call = {"name": "book_slot",
            "arguments": {"date": "2026-11-14", "minutes": 90}}
    ok, reason = tools.valid(call)
    if not ok:
        return {"reply": "Tool refused: " + reason, "options": [],
                "action": None, "unsupported_claims": []}
    PENDING_TOOL = call
    description = tools.describe(call)
    return {"reply": description, "options": [], "action": None,
            "unsupported_claims": [], "tool_call": call,
            "tool_confirmation": description}
```

After the existing model call has returned its `data` dictionary, keep the model's error fallback if
the reply is malformed. Do not let retrieval hide that recovery message:

```python
data = model.call_json(parts, SCHEMA)
if not valid(data):
    return fallback_turn()
```

For a valid response, use the highest-ranked current passage as the local mock's answer. If the top
retrieval result is marked superseded, show the current passage as the answer, warn that the retriever
ranked an old passage first, and keep both passages visible so you can inspect the failure. Do not
present zero-score passages as evidence:

```python
hits = retrieve.retrieve(message, k=3)
relevant = [h for h in hits if h["score"] > 0]
if relevant and relevant[0]["score"] >= 0.25:
    top = relevant[0]
    if top.get("superseded"):
        current = next((h for h in relevant
                        if h["section"] == top["section"] and not h.get("superseded")), None)
        if current:
            data["reply"] = current["text"]
            data["stale_warning"] = "The top retrieval result is superseded. This answer uses the newer passage shown below."
        else:
            data["reply"] = "The top result is marked superseded, and no current passage was found. Check a current source before using it."
            data["stale_warning"] = "No current passage was found; do not rely on the old result."
    else:
        data["reply"] = top["text"]
else:
    data["reply"] = "The supplied corpus does not give a reliable answer. Ask the module lead about anything it does not cover."
data["options"] = []
data["action"] = None
data["evidence"] = relevant
return data
```

Keep the existing response shape. The local mock uses the retrieved passage for this route; a live
model route would need to receive the quoted passages as context and still show their provenance.

## 2. Add the visible controls to `index.html`

Add these buttons above the message input:

```html
<p><button onclick="send('__poster__')">Test poster image</button>
<button onclick="send('__noticeboard__')">Test noticeboard image</button>
<button onclick="send('book a revision slot')">Propose revision slot</button></p>
```

Inside `render(data)`, after the existing option buttons and before the final note, add:

```javascript
if (data.reply && !data.tool_confirmation && !data.tool_result) {
  const answer = document.createElement('p');
  answer.textContent = data.reply;
  card.appendChild(answer);
}

if (data.evidence && data.evidence.length) {
  const e = document.createElement('div');
  e.className = 'card';
  e.innerHTML = '<strong>Evidence</strong>';
  data.evidence.forEach(h => {
    const p = document.createElement('p');
    p.textContent = (h.superseded ? '[SUPERSEDED | ' : '[') + h.source + ' | ' + h.section +
      ' | updated ' + h.date + ' | score ' + h.score + '] ' + h.text;
    e.appendChild(p);
  });
  card.appendChild(e);
}

if (data.stale_warning) {
  const warning = document.createElement('p');
  warning.className = 'warning';
  warning.setAttribute('role', 'alert');
  warning.textContent = data.stale_warning;
  card.appendChild(warning);
}

if (data.tool_confirmation) {
  const p = document.createElement('p');
  p.textContent = data.tool_confirmation;
  card.appendChild(p);
  const yes = document.createElement('button');
  yes.textContent = 'Confirm';
  yes.onclick = () => send('__confirm_tool__');
  card.appendChild(yes);
  const no = document.createElement('button');
  no.textContent = 'Cancel';
  no.onclick = () => send('__cancel_tool__');
  card.appendChild(no);
}

if (data.tool_result) {
  const result = document.createElement('p');
  result.textContent = 'Tool result: ' + JSON.stringify(data.tool_result);
  card.appendChild(result);
}
```

In the supplied starter, `.warning` is already styled as a visible alert. If you kept your own Lab 3
interface, add equivalent styling so the superseded-source warning stands out from the evidence text.

In the `send(text)` function, keep internal button commands out of the visible transcript by changing
`say(text, true);` to `if (!text.startsWith('__')) say(text, true);` before the `fetch` call.

## 3. Run the browser checks

Run `python app.py`, open `http://localhost:8000`, and check these in order. Use the buttons you added
to the page for the image and tool checks:

1. Type `when is coursework 1 due`. The result card must show an answer and evidence with text,
   source, section, date and score.
2. Select **Propose revision slot**. Check the date and minutes, then select **Confirm**. The card
   must show the tool result, and `tool_log.jsonl` must contain the same call. Try the invalid
   `minutes: 900` call in `tools.py`; it must be refused and must not be logged as successful.
3. Select **Test poster image**. The card must show `14 November, 12:00` and a confidence.
4. Select **Test noticeboard image**. The card must show the refusal reason. It must not invent a date
   or read out the person's mark.

If one of these appears only in the terminal, the phase is not complete.
