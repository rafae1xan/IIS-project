# One Glance Control

README prose word count: 536 (headings, code and setup commands excluded; bullet text included).

## Project status

This repository contains the A2 project prototype for inspecting evidence and proposed actions in an action-oriented LLM system.

Implemented locally:

- a runnable browser interface with an evidence and control panel;
- retrieval with quoted passages, source, section, date, score and superseded-source warnings;
- a structured action preview with object, parameters, impact, uncertainty and reversibility;
- validation before execution, Confirm/Cancel control and a local tool log;
- refusal for unsupported or ambiguous requests;
- a mock image answer with confidence and a refusal case.

Simulated: the model, course corpus, image model and local revision-schedule tool. The prototype does not contact an external calendar or store personal data.

Planned: a permissioned calendar connector, editable action parameters, authentication and a small user comparison of generic confirmation against the structured panel.

## Technology stack

Python 3 standard library serves the local app. `retrieve.py` implements a small lexical retriever; `tools.py` validates and runs one narrow local schedule operation; `vlm.py` provides the supplied offline image teaching cases; `index.html` is the browser interface. ChatGPT supported design/report brainstorming and GitHub Copilot supplied some boilerplate; the runtime uses a mock model rather than an external LLM so the route is reproducible without an API key. A future connected version still needs a model/API choice and a permissioned calendar connector.

## Running or inspecting the work

```text
python app.py
```

Open the local address printed in the terminal. The scripted walkthrough is in `demo_walkthrough.md`. The architecture, storyboard, interface-state, run-log and code-evidence images are in `assets/`. `capture_ui_states.html` and `capture_ui.cjs` reproduce the three captured interface states; `recorded_runs/a2_run_log.txt` records the executed evidence checks.

Self-checks:

```text
python retrieve.py --selftest
python tools.py --selftest
python vlm.py --selftest
```

## Development record

- 2026-10-21: reviewed the Assignment 1 literature and feedback; narrowed the project from general LLM trust to a testable evidence-to-action boundary.
- 2026-10-25: translated Lab 3 concepts into the control-panel fields for evidence, selected object, parameters, impact, uncertainty and reversibility; checked that the fields support comparison before execution.
- 2026-10-29: integrated the supplied Lab 4 offline route, local corpus, mock responses and validation helpers so the prototype could run without an API key; ran the baseline retrieval, tool and image self-tests.
- 2026-11-02: added provenance display, stale-source repair and unsupported-claim refusal after testing showed that a top-ranked passage was not always the current source.
- 2026-11-05: added the structured action proposal, Confirm/Cancel gate and tool-result logging; checked that an invalid 900-minute call is refused before execution and that cancellation produces no file change.
- 2026-11-07: created the system diagram, normal/failure storyboards and three interface-state captures; replayed grounded, stale, ambiguous, confirmed and image-refusal cases.
- 2026-11-08: assembled the report evidence, added the run-log and code-excerpt figures, checked the abstract/main word counts and corrected the Figure 5 JSON wrapping.

Public GitHub repository: https://github.com/rafae1xan/IIS-project

README: https://github.com/rafae1xan/IIS-project/blob/main/README.md

Submitted release tag: `v0.1` — https://github.com/rafae1xan/IIS-project/releases/tag/v0.1

The submitted development evidence is recorded in this README's Development record section. If the public repository uses a different final tag or commit, replace the tag above with the exact submitted identifier.

## AI assistance

I used ChatGPT to brainstorm the control-panel fields, suggest report structure and improve clarity. I checked its suggestions against the Lab 3/4 materials and my implementation, rewrote the text in my own words, and removed claims that the prototype does not support. I used GitHub Copilot for some boilerplate code; I reviewed and modified the code and ran the valid, invalid, ambiguous and stale-source cases to confirm the logged outputs. All design choices, claims and references are my responsibility.

## Additional files

The A2 report is submitted separately and links to this README. The accompanying ZIP is a snapshot of this project; unzip it and follow the Running or inspecting the work section. The `assets/` folder contains the system diagram, storyboards, three interface-state captures, the run-log capture and the code excerpt. `recorded_runs/a2_run_log.txt` contains the command outputs and interaction checks used in the report. `capture_ui_states.html` and `capture_ui.cjs` are the reproducible capture helpers; `build_evidence.py` generates the run-log and code-evidence figures.
