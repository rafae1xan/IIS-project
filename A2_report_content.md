# One Glance Control for Action Oriented LLM Systems

**A2 Project Report**  
**Abstract: 173 words | Main report: 950 words | Total counted text: 1,123 words**

## Abstract

Action-oriented LLM systems can interpret a natural-language request, retrieve information and propose an external action. Their fluency can make an unsupported interpretation look safe, while a generic confirmation button hides the object, parameters and consequences being approved. This project develops One-Glance Control, a local prototype for inspecting the evidence-to-action boundary before execution. The interface shows quoted evidence and provenance for answers, then presents a proposed action with its selected object, parameters, impact, uncertainty and reversibility. A validation gate rejects malformed calls; a user confirmation is required before the narrow local scheduling tool runs. The prototype also demonstrates stale-source warnings, refusal when the corpus cannot support a claim and recovery from ambiguous requests. Its current scope is a simulated revision-scheduling task using a local corpus and mock model. A live calendar connector, authenticated permissions and a user study are planned rather than claimed as implemented. The project asks whether a compact, structured pre-action view can preserve control without returning the full verification burden to the user.

## Project scope and developed work

The project follows the opportunity identified in Assignment 1: compare pre-action confirmation mechanisms that connect evidence, model decisions and execution. The developed scope is a single offline assistant route. A person can ask a question, request a revision slot, inspect a proposed local schedule change, confirm or cancel it, and see the returned result. The prototype uses the supplied Lab 4 corpus and mock model so that the interaction is reproducible without an API key. Retrieval, provenance display, structured action data, validation, confirmation, refusal and logging are implemented. The model response, local corpus and local schedule file are simulations of a future connected system; no external calendar or personal data is accessed.

## Design rationale and project explanation

The central design choice is to treat control as a visible interaction state rather than as a final button. Assignment 1 showed that mixed-initiative interaction, grounding, explanation and tool architecture address different parts of the same delegation problem. Horvitz (1999) describes a trade-off between assistance and interruption, while Clark and Brennan (1991) describe grounding as understanding sufficient for the current purpose. In this prototype, the assistant may take initiative by preparing a proposal, but it cannot silently convert a plausible interpretation into a side effect. The user sees what object was selected, which parameters will be used and what will change before execution.

The control panel therefore has two related views. For an information request, it shows the answer beside the quoted passages used to produce it, including source, section, date and retrieval score. This implements the Week 4 emphasis on retrieval, grounding and provenance. A score is labelled as a relative ranking signal rather than a probability. When an older passage ranks first, the interface marks it as superseded, keeps the older result visible for inspection and bases the answer on the newer passage. When no sufficiently relevant passage is available, it refuses to answer and gives a next step. This addresses the limitation identified in Assignment 1: evidence is useful only when the user can inspect whether it supports the actual claim.

For an action request, the panel presents a structured preview instead of a vague “Are you sure?” message. The preview identifies the selected object, date, duration, impact, uncertainty and reversibility. This draws on the Week 2 topics of mental models, feedback, action error, agency and decision. Showing the important fields together reduces the need to remember the original request while comparing it with the proposed change. The result also makes an error repairable: the user can cancel, clarify the request or correct a parameter before the tool runs. Kulesza et al. (2013) warn that explanations can be too sparse or too detailed; the design consequently exposes decision-relevant evidence and consequences, rather than a long generic rationale.

The model-system boundary is explicit. Week 3 treats prompting as specifying and checking a model call, while Week 4 distinguishes model proposals from tools and connectors. The prototype follows that separation: the model or mock produces a proposal, `tools.valid` checks its shape, date and duration, and only a confirmed valid call reaches `tools.run`. The invalid 900-minute example is refused before execution. The tool writes one local schedule entry and records the arguments, confirmation and returned result in `tool_log.jsonl`. Reporting from the tool result, rather than from the model sentence, prevents a fluent claim of success from replacing evidence that the action happened.

The interface also includes two recovery paths. An ambiguous appointment request produces selectable options rather than choosing an object by guess. A request involving an unsupported clinic or unavailable days produces a refusal and explicitly lists the unchecked claim. These behaviours apply the Week 2 focus on feedback and error recovery and the Week 3 focus on asking for missing information. The image demonstration extends the same principle: a supported poster question displays a confidence and evidence, while an unrelated noticeboard question is refused because the image cannot answer it and contains personal data. These are simulated teaching cases, not a claim of general visual reliability.

The main trade-off is compactness versus completeness. One glance cannot show every model operation, and a provenance panel can still be too dense for a high-stakes decision. I therefore prioritised the fields that change whether a person should proceed: selected object, parameters, supporting passage, uncertainty, impact and reversibility. A live system would need domain-specific risk rules, permission checks, idempotency and a clear distinction between reversible and irreversible actions. Those are planned extensions, not hidden assumptions.

## Developed interaction and evidence

Figure 1 shows the system boundary and control flow. Figures 2 and 3 show the normal path and a stale-source recovery path. The runnable repository demonstrates the same states: an evidence answer, a superseded-source warning, a pending confirmation, a cancelled proposal, a confirmed local tool result, an invalid call refusal and an unanswerable request. The implementation is intentionally modest so that a reader can inspect the complete path rather than infer behaviour from a list of planned features.

## Development decisions and current limits

The project developed from the Assignment 1 literature map into the Lab 3 system-path exercise and the Lab 4 retrieval/tool integration. The supplied mock route was retained because it makes the project reproducible and keeps the system boundary visible. The interface and response shape were then changed to make evidence, action parameters and control state first-class fields. The next development stage would replace the local corpus with a permissioned connector and run a small comparison of generic confirmation versus the structured control panel, measuring error detection, completion time and unnecessary cancellation. Until then, the prototype supports a design argument and walkthrough, not a causal evaluation.

## References

Clark, H. H., & Brennan, S. E. (1991). Grounding in communication. In *Perspectives on socially shared cognition*.

Horvitz, E. (1999). Principles of mixed-initiative user interfaces. *CHI 1999*, 159–166.

Ji, Z., et al. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys*, 55(12), 1–38.

Kulesza, T., et al. (2013). Too much, too little, or just right? Ways explanations impact end users’ mental models. *IEEE VL/HCC*, 3–10.

Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS 33*.

Luger, E., & Sellen, A. (2016). “Like having a really bad PA”: The gulf between user expectation and experience of conversational agents. *CHI 2016*, 5286–5297.

Shi, F., et al. (2023). Large language models can be easily distracted by irrelevant context. *ICML 2023*.

Shneiderman, B. (2022). *Human-centered AI*. Oxford University Press.

University of Birmingham. (2026). *LH/LM Intelligent Interactive Systems: Weeks 1–4 lecture slides and lab materials*. Canvas course materials.

## Figures

**Figure 1.** System boundary, components and control flow. Green components are implemented locally; amber components are simulated.

**Figure 2.** Normal interaction: inspect, decide and receive the tool result.

**Figure 3.** Failure and recovery: stale evidence is exposed and the decision returns to the person.
