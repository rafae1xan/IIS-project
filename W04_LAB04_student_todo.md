# Lab 4 — Student To-Do
## LLM/VLM Integration, Retrieval and Tool Use

### Goal

By the end of the lab you should have:

- a context map showing what is actually sent to the model;
- one grounded answer with the **quoted passage, source, date and score** shown;
- one narrow tool that is **validated, confirmed, executed and logged**;
- one image question answered with a visible confidence;
- one image case correctly refused with a reason;
- a three-row test record containing:
  - one grounded case,
  - one stale case,
  - one unanswerable case.

The supplied mock is the route used for the checks in this lab.

---

<!-- AI-ACCESS-BLOCK-A -->
## Which AI tool?

If you use an external AI tool for your own project route, record what you used and what you changed
about its output. The supplied checks use the starter's mock and sample material.

| What you need it for | Tool | Cost and catch |
|---|---|---|
| Chat, drafting, explanation, study support | **Gemini for Students** — <https://gemini.google/students/> | Free for eligible university students aged 18+, for one year, verified annually. Redeem by 31 December 2026. **It renews at £4.49/month unless you cancel.** Set a calendar reminder the day you sign up. |
| A model your **code** calls | **Google AI Studio** (Gemini API free tier) | Free tier, no card. The student plan above does **not** include API access — these are different products. |
| An agent that works inside your repository | **Gemini CLI** | Free with a personal Google account: 60 requests/minute, 1,000 per day, no API key. It reads and edits files and runs commands. |

Any equivalent is fine — Claude, ChatGPT, GitHub Copilot, or a local model through Ollama or
LM Studio. The course comparison sheet lists the free options with their limits.

**Two rules, whichever route you take.**

1. **Record what you used.** Which tool, which route, and what you changed about what it gave you.
   An undeclared tool is the problem; a declared one never is.
2. **Nothing confidential goes into a personal free account.** No participant data, no one else's
   personal data, no unpublished work that is not yours to share. A consumer free plan is not an
   institutional agreement, and this module asks you to know the difference.

---

# FILES YOU WILL USE

From the Lab 4 starter:

- `01_CONTEXT_MAP.md`
- `retrieve.py`
- `corpus/`
- `tools.py`
- `vlm.py`
- `sample_images/`
- `02_TEST_RECORD.md`
- `demo_walkthrough.md`
- `W04_LAB04_integration_steps.md`

If your Lab 3 app runs, you can copy the Lab 4 support files into that project and keep its app files.
If you do not have a working app, use the runnable `app.py`, `model.py` and `index.html` included in
this pack. You can complete the whole lab with that project; Lab 3 is not required. Work in one project
folder and do not mix files from different copies.

Before copying them, run your existing Lab 3 prototype and make one ordinary request. If it runs, keep
the Lab 3 entry point and interface files, including `app.py`, `model.py` and `index.html` or their
equivalents. If you do not have a runnable app, copy the complete project from this pack into a folder
of your own and start there.

---

# STEP 0 — CHECK THE STARTER

Run:

```bash
python retrieve.py --selftest
python tools.py --selftest
python vlm.py --selftest
```

Expected:

```text
ok: 6 documents, 14 passages
ok: valid call accepted, 900-minute call refused
ok: 2 sample images
```

Use the supplied mock and starter material for the checks in this lab. Do not spend the lab
configuring an unconfirmed external service.

---

# HOW LAB 4 CONNECTS TO YOUR PROTOTYPE

You are extending the app in your project folder. That may be your working Lab 3 app or the supplied
fallback app. In the supplied prototype:

- `app.py` receives the message and returns a response dictionary from `turn(message)`;
- `index.html` receives that dictionary in `render(data)` and draws the answer card.

For each Lab 4 feature, pass the new result in that dictionary and render it in `index.html`. A terminal
result alone is not enough for the phase to be complete.

Use this route:

1. **Retrieval:** call `retrieve.retrieve(message, k=3)` in `app.py`, keep the returned text, source,
   section, date and score, and add them to the response as an evidence list. In `index.html`, render
   the evidence list beside the answer.
2. **Tool:** use `tools.valid(call)` before `tools.run(call)`. Use `tools.describe(call)` for the
   confirmation text. Show that text and a Confirm/Cancel choice in the result card; call `tools.run`
   only after Confirm, then display the returned result and check `tool_log.jsonl`.
3. **Image:** call `vlm.ask(image_path, question)` in `app.py`. Pass either its claim, confidence and
   evidence or its refusal reason into the response dictionary. In `index.html`, render the confidence
   for the answer case and the refusal reason for the noticeboard case.

After each change, run `python app.py`, open <http://localhost:8000>, make the test request in the
browser and check the screen. If the result appears only in the terminal, that phase is not complete.

---

# STEP 1 — PRINT THE CONTEXT YOU ACTUALLY SEND
## Start here: `app.py` in your project folder

Open `app.py` and find the function that sends the request to the model. In the canonical Lab 3 starter
this is `turn(message)`, immediately before `model.call_json(...)`; your project may use an equivalent
function. Inspect the actual list passed to the model. The supplied starting app sends only the current
user message at this point; it has no history, tool definitions or retrieved passages yet. Make the
inline request list a named variable and add this helper:

```python
def log_context(parts):
    for part in parts:
        print("CONTEXT:", part)
```

Then pass the named `parts` variable to the model call. `01_CONTEXT_MAP.md` is the file where you record
what you find; it is not the file that assembles the context.

Add the logging call, then run your normal Lab 3 app command and make one ordinary request in the
interface. Read the context output in the terminal. The canonical starter is run with:

```bash
python app.py
```

Open <http://localhost:8000> if the terminal reports that the server is running there.

Look at what is actually being sent. Do not invent context parts that are absent.

Record each part in `01_CONTEXT_MAP.md`:

- instructions;
- conversation/history;
- retrieved passages;
- tool definitions;
- anything else your prototype adds.

For each part write:

- where it comes from;
- whether it is trusted;
- roughly how much space it uses.

If your app has a redundant part, remove it only if the request still works. The supplied starting app
has only the current user message, so there is nothing safe to remove at this stage. Record that in the
map and revisit the context after you add retrieval in Step 2. Removing a part is optional when there is
nothing redundant.

Examples:

- old turns already represented by a summary;
- a tool definition for a tool you do not use;
- duplicated instructions.

If you remove a part, run `python app.py` again and make the same request to check that it still works.
If there was nothing safe to remove, keep the original context and review it again after retrieval is
added.

### Done when

- [ ] `01_CONTEXT_MAP.md` has one row per context part
- [ ] you identified what came from you and what came from outside, and marked absent context as `not present`
- [ ] you recorded what is and is not in the context; remove a part only if it is redundant
- [ ] you recorded one context change and checked it in the browser

---

# STEP 2 — RUN RETRIEVAL ON ITS OWN
## Start here: `retrieve.py` from the Lab 4 starter

Before wiring retrieval into the interface, test it directly.

Example:

```bash
python retrieve.py "when is coursework 1 due"
```

Each hit should contain:

- passage text;
- source;
- section;
- date;
- score.

Important:

> The score is a ranking signal, not a probability.

Now try a question relevant to your own project.

Use 5–10 short documents in `corpus/`, or use the supplied six documents for today.

---

# STEP 3 — SHOW PROVENANCE BESIDE THE ANSWER
## Start here: the answer-rendering part of your app interface

Return to the function that displays the model answer in your existing prototype. Keep the retrieval
metadata from Step 2 and render it beside the answer there.

Wire retrieval into your existing prototype.

The screen should show the answer **and the source passage used to support it**.

Show:

- quoted passage;
- source;
- section if available;
- date;
- retrieval score.

Do **not** throw away the source metadata and paste only the passage text into the context.

Ask yourself:

> Could a classmate check this claim without asking me anything?

If not, the provenance is not visible enough.

### Done when

A question in the browser shows:

- [ ] answer
- [ ] quoted passage
- [ ] source
- [ ] date
- [ ] score

---

# STEP 4 — TEST A STALE SOURCE
## Start here: `corpus/handbook.md` and `corpus/handbook_late.md`

Use the supplied stale/current handbook documents.

Try:

```text
What is the late-submission penalty?
```

The retriever may rank the old document first. The interface should mark that source as superseded,
warn you, and use the newer passage as its answer when one is available. Check both the warning and
the two source dates, then record what the retriever ranked first and what the page used for its answer.

This case will go into `02_TEST_RECORD.md`.

The important lesson:

> A real, correctly quoted source can still be wrong because it is stale.

---

# STEP 5 — ADD ONE NARROW TOOL
## Start here: `tools.py` from the Lab 4 starter

The starter contains:

```text
book_slot
```

It adds one revision slot to a local schedule.

You may use that, or define one similarly narrow tool for your own system.

A good tool has:

- one operation;
- explicit arguments;
- clear limits;
- a defined result.

Bad:

```text
access my calendar
```

Better:

```text
add one revision slot to this local schedule
```

---

# STEP 6 — VALIDATE BEFORE EXECUTION
## Start here: the validation function in `tools.py`

Use the `valid(call)` check before the code that executes a tool call. The invalid example below should
stop at that check and must not reach the tool runner.

Test an invalid proposal.

For the starter tool:

```json
{
  "name": "book_slot",
  "arguments": {
    "date": "2026-11-14",
    "minutes": 900
  }
}
```

Expected:

```text
refused: minutes must be between 15 and 180
```

Nothing should run.

### Rule

> A malformed or invalid call is a caught error, never an action.

---

# STEP 7 — CONFIRM WITH THE ARGUMENTS VISIBLE
## Start here: the confirmation step immediately after validation

Use the valid call from Step 6. Add the confirmation before the tool runner, so the user sees the
arguments and consequence before anything runs.

For a valid proposal, show the action in human-readable form before executing it.

Example:

```text
Add a 90-minute revision slot on Sat 14 Nov 2026?

[ Confirm ] [ Cancel ]
```

Do not use only:

```text
Are you sure?
```

The user must see the **arguments and consequence** they are approving.

---

# STEP 8 — RUN, LOG, REPORT FROM THE RESULT
## Start here: the tool runner and `tool_log.jsonl`

Continue from the confirmed call in Step 7. The runner returns the result; write that result to
`tool_log.jsonl` and report it in the interface.

After confirmation:

1. run the tool;
2. write a log entry;
3. report what the tool actually returned.

The starter writes:

```text
tool_log.jsonl
```

A log entry should include:

- tool name;
- arguments;
- who confirmed;
- result.

Check:

```bash
tail -1 tool_log.jsonl
```

### Important

Do not report success from the model's sentence.

Report from the tool result.

---

# STEP 9 — RUN THE VLM ANSWER CASE
## Start here: `vlm.py` and `sample_images/sample_poster.png`

Run:

```bash
python vlm.py sample_images/sample_poster.png "what deadline is shown?"
```

The result should contain:

- claim;
- confidence;
- evidence.

Render the confidence **on the page**, not only in the terminal.

### Done when

The user can see both:

```text
14 November, 12:00
confidence 0.86
```

or equivalent.

---

# STEP 10 — RUN THE VLM REFUSAL CASE
## Start here: `sample_images/sample_noticeboard.png`

Run the same question on:

```text
sample_images/sample_noticeboard.png
```

The system should refuse because:

1. the image does not contain the requested deadline;
2. the image contains a named person's mark/personal data.

Do not treat the refusal as a bug.

Do not make the model guess a deadline.

Do not use a photograph of a real person for this exercise.

---

# STEP 11 — COMPLETE `02_TEST_RECORD.md`
## Start here: the three runs you have just completed

Use the outputs from Steps 3, 4 and 10 rather than inventing expected results. `02_TEST_RECORD.md` is the
record of what happened; it is not another implementation task.

Run three questions:

### 1. Grounded
A question your corpus genuinely answers.

### 2. Stale
A question answered by an out-of-date source.

### 3. Unanswerable
A question your corpus does not cover.

Record what the **screen actually showed**, not what you intended it to show.

Template:

| question | type | what the screen showed | right? | what I would change |
|---|---|---|---|---|

If the result is wrong or only partly right, say so and write a concrete change. For the supplied stale
case, the ranking is still wrong even though the interface warns you and uses the current passage.
Your record can say `partly` and explain both points.

A row can honestly say:

```text
no
```

A failed case with a concrete fix is useful evidence.

---

# BEFORE YOU LEAVE

Check:

- [ ] `01_CONTEXT_MAP.md` completed
- [ ] the context map records any removal, or says there was nothing redundant to remove
- [ ] grounded answer shows passage + source + date + score
- [ ] one invalid tool call refused without running
- [ ] confirmation shows arguments
- [ ] successful tool call logged in `tool_log.jsonl`
- [ ] report built from tool result
- [ ] one image answer shows confidence
- [ ] one image is correctly refused with a reason
- [ ] `02_TEST_RECORD.md` has grounded, stale and unanswerable rows
- [ ] no API keys committed
- [ ] no real personal/confidential documents committed
- [ ] no photographs of real people used

Save/push the repository somewhere you can access next week.

---

# THE WHOLE LAB IN ONE LINE

**Inspect context → retrieve evidence → show provenance → validate and confirm one action → report from the tool result → answer/refuse one image → record three real test outcomes**
