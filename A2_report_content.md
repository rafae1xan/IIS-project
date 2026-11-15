# One Glance Control for Action Oriented LLM Systems

**A2 Project Report**  
**Abstract: 165 words | Main report: 1,059 words | Total counted text: 1,224 words**

## Abstract

Action-oriented LLM systems can interpret a natural-language request, retrieve information and propose an external action. Their fluency can make an unsupported interpretation look safe, while a generic confirmation button hides the object, parameters and consequences being approved. This project develops One-Glance Control, a local prototype for inspecting the evidence-to-action boundary before execution. The interface shows quoted evidence and provenance for answers, then presents a proposed action with its selected object, parameters, impact, uncertainty and reversibility. A validation gate rejects malformed calls; a user confirmation is required before the narrow local scheduling tool runs. The prototype also demonstrates stale-source warnings, refusal when the corpus cannot support a claim and recovery from ambiguous requests. Its current scope is a simulated revision-scheduling task using a local corpus and mock model. A live calendar connector, authenticated permissions and a user study are planned rather than claimed as implemented. The project asks whether a compact, structured pre-action view can preserve control without returning the full verification burden to the user.

## Project scope and developed work

The project follows the opportunity identified in Assignment 1: compare pre-action confirmation mechanisms that connect evidence, model decisions and execution. Feedback narrowed the problem to a testable evidence-to-action boundary. The developed scope is a single offline assistant route. A person can ask a question, request a revision slot, inspect a proposed local schedule change, confirm or cancel it, and see the returned result. The prototype uses the supplied Lab 4 corpus and mock model so that the interaction is reproducible without an API key. Retrieval, provenance display, structured action data, validation, confirmation, refusal and logging are implemented. The model response, local corpus and local schedule file are simulations of a future connected system; no external calendar or personal data is accessed.

## Design rationale and project explanation

The central design choice is to treat control as a visible interaction state rather than as a final button. Assignment 1 showed that mixed-initiative interaction, grounding, explanation and tool architecture address different parts of the same delegation problem. Horvitz (1999) describes a trade-off between assistance and interruption, while Clark and Brennan (1991) describe grounding as understanding sufficient for the current purpose. In this prototype, the assistant may take initiative by preparing a proposal, but it cannot silently convert a plausible interpretation into a side effect. The user sees what object was selected, which parameters will be used and what will change before execution.

The control panel therefore has two related views. For an information request, it shows the answer beside the quoted passages used to produce it, including source, section, date and retrieval score. This implements the Week 4 emphasis on retrieval, grounding and provenance. A score is labelled as a relative ranking signal rather than a probability. When an older passage ranks first, the interface marks it as superseded, keeps the older result visible for inspection and bases the answer on the newer passage. When no sufficiently relevant passage is available, it refuses to answer and gives a next step. This addresses the limitation identified in Assignment 1: evidence is useful only when the user can inspect whether it supports the actual claim.

For an action request, the panel presents a structured preview instead of a vague “Are you sure?” message. The preview identifies the selected object, date, duration, impact, uncertainty and reversibility. This draws on the Week 2 topics of mental models, feedback, action error, agency and decision. Showing the important fields together reduces the need to remember the original request while comparing it with the proposed change. The result also makes an error repairable: the user can cancel, clarify the request or correct a parameter before the tool runs. Kulesza et al. (2013) warn that explanations can be too sparse or too detailed; the design consequently exposes decision-relevant evidence and consequences, rather than a long generic rationale.

The model-system boundary is explicit. Week 3 treats prompting as specifying and checking a model call, while Week 4 distinguishes model proposals from tools and connectors. The prototype follows that separation: the model or mock produces a proposal, `tools.valid` checks its shape, date and duration, and only a confirmed valid call reaches `tools.run`. The invalid 900-minute example is refused before execution. The tool writes one local schedule entry and records the arguments, confirmation and returned result in `tool_log.jsonl`. Reporting from the tool result, rather than from the model sentence, prevents a fluent claim of success from replacing evidence that the action happened.

The interface also includes two recovery paths. An ambiguous appointment request produces selectable options rather than choosing an object by guess. A request involving an unsupported clinic or unavailable days produces a refusal and explicitly lists the unchecked claim. These behaviours apply the Week 2 focus on feedback and error recovery and the Week 3 focus on asking for missing information. The image demonstration extends the same principle: a supported poster question displays a confidence and evidence, while an unrelated noticeboard question is refused because the image cannot answer it and contains personal data. These are simulated teaching cases, not a claim of general visual reliability.

The main trade-off is compactness versus completeness. One glance cannot show every model operation, and a provenance panel can still be too dense for a high-stakes decision. I therefore prioritised the fields that change whether a person should proceed: selected object, parameters, supporting passage, uncertainty, impact and reversibility. A live system would need domain-specific risk rules, permission checks, idempotency and a clear distinction between reversible and irreversible actions. Those are planned extensions, not hidden assumptions.

## Developed interaction and evidence

Figure 1 shows the system boundary and control flow. Figures 2 and 3 show the normal path and stale-source recovery. The repository demonstrates grounded answers, pending confirmation, cancellation, confirmed execution, invalid-call refusal and unanswerable-image refusal.

## Storyboards and illustrated interaction

The storyboard and interface captures document three concrete uses.

1. Proposal: the person types “book a revision slot”; the system shows object, date, duration, impact and reversibility with Confirm/Cancel. Nothing changes yet (Figures 2 and 4).

2. Execution or recovery: Confirm writes one local entry and reports JSON; Cancel returns “No action was taken” (Figure 5).

3. Evidence repair: the late-submission query exposes an older passage, a newer date and a superseded warning instead of silently replacing evidence (Figures 3 and 6).

## Runtime and implementation evidence

Figures 4-6 show the same HTML layout populated with real `app.turn` response states: awaiting confirmation, executed result and stale-source repair. Figure 7 records the self-tests: 6 documents/14 passages, valid-call acceptance, 900-minute refusal before execution and 2 checked sample images. It also records confirmation, cancellation and image refusal.

Figure 8 shows `app.py`: validation stores a proposal in `PENDING_CALL`, while `tools.run` appears only in `confirm_tool` after confirmation.

## Development decisions and current limits

The work changed in stages. Assignment 1 feedback narrowed the problem from general LLM trust to a testable evidence-to-action boundary. Lab 3 made evidence, object, parameters, impact, uncertainty and reversibility visible in one panel. Lab 4 supplied the offline route; tests then prompted stale-source repair, refusal and confirmation as implemented states. Final checks covered grounded, stale, valid, invalid, ambiguous, cancelled, confirmed and image-refusal cases. This applies Week 1 human-centred framing, Week 2 feedback and agency, Week 3 model-tool separation and Week 4 provenance (University of Birmingham, 2026). A future study would compare this panel with generic confirmation; this prototype is not causal evidence.

## Repository and development evidence

Public GitHub repository: https://github.com/rafae1xan/IIS-project

README: https://github.com/rafae1xan/IIS-project/blob/main/README.md

Submitted release tag: v0.1 (https://github.com/rafae1xan/IIS-project/releases/tag/v0.1)

For the development record, setup instructions and test evidence, see the Development record section of the README.

## References

Clark, H. H., & Brennan, S. E. (1991). Grounding in communication. In *Perspectives on socially shared cognition*.

Horvitz, E. (1999). Principles of mixed-initiative user interfaces. *CHI 1999*, 159–166.

Kulesza, T., et al. (2013). Too much, too little, or just right? Ways explanations impact end users’ mental models. *IEEE VL/HCC*, 3–10.

University of Birmingham. (2026). *LH/LM Intelligent Interactive Systems: Weeks 1–4 lecture slides and lab materials*. Canvas course materials.

Reused material: the offline corpus, mock route and validation helpers from the supplied Lab 4 materials were retained and adapted. The report prose, figure labels and additional evidence captures are original project work.

## Figures

**Figure 1.** System boundary, components and control flow. Green components are implemented locally; amber components are simulated; purple items are planned.

**Figure 2.** Normal interaction: inspect, decide and receive the tool result.

**Figure 3.** Failure and recovery: stale evidence is exposed and the decision returns to the person.

**Figure 4.** Interface capture: an action proposal is visible before execution.

**Figure 5.** Interface capture: the confirmed local tool result and executed state.

**Figure 6.** Interface capture: stale evidence, provenance and superseded-source warning.

**Figure 7.** Recorded self-test and interaction log.

**Figure 8.** Code excerpt showing validation, pending state and confirmation-gated execution.
