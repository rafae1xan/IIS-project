# One Glance Control

README prose word count: 245 (code and setup commands excluded).

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

Python 3 standard library serves the local app. `retrieve.py` implements a small lexical retriever; `tools.py` validates and runs one narrow local schedule operation; `vlm.py` provides the supplied offline image teaching cases; `index.html` is the browser interface. No API key is required.

## Running or inspecting the work

```text
python app.py
```

Open the local address printed in the terminal. The scripted walkthrough is in `demo_walkthrough.md`. The architecture and storyboard images are in `assets/`.

Self-checks:

```text
python retrieve.py --selftest
python tools.py --selftest
python vlm.py --selftest
```

## Development record

- 2026-11-06: started from the supplied Lab 4 offline route and retained its local corpus, mock responses and validation helpers so the work is reproducible.
- 2026-11-06: changed the interface to make evidence, selected object, parameters, impact, uncertainty and reversibility visible in one control panel.
- 2026-11-06: added stale-source repair, unsupported-claim refusal, explicit Confirm/Cancel state and reporting from the tool result.
- 2026-11-06: created the system diagram and normal/failure storyboards; ran Python syntax checks and all three supplied self-tests.

Local release: `v0.1` (create or update the submitted Git commit after copying this folder to the public repository).

Public GitHub repository: **add the repository URL here before submission**.

## AI assistance

OpenAI Codex was used to help inspect the Canvas brief and supplied lab materials, implement the local prototype changes, draft the report structure and create the diagrams. The output was checked against the A2 requirements and the supplied Lab 4 self-tests. The project scope, status labels, design claims and references were reviewed and corrected so that simulated components are not presented as live integrations.

## Additional files

The A2 report is outside this repository's code route and links to this README. The `assets/` folder contains the report figures. No ZIP-only material is required.
