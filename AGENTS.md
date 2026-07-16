# Project Instructions

## Purpose

This repository records a beginner-friendly learning journey through quantum error correction (QEC) and surface codes. The primary objective is conceptual understanding that supports communication with researchers. QEC DSL, compiler, hardware ISA, and binary encoding remain a later engineering track and must not displace the current learning sequence.

## Teaching Style

- Teach in Chinese while retaining important English terms used by papers and engineers.
- Assume the learner has almost no mathematics or physics background. Do not infer prerequisite knowledge from the learner's quantum-control software job title or from concepts not explicitly demonstrated during this course.
- Before using any new term or symbol, explain it in plain language with a concrete, observable example. Never use one undefined term, such as amplitude, phase, interference, eigenstate, or tensor product, to explain another.
- Teach only one new conceptual step at a time and check that step before continuing. If an explanation is unclear, discard it and restart from the missing prerequisite instead of adding more jargon or formulas.
- Separate an operational description (what is prepared, what operation is performed, and what is observed) from the mathematical model. Introduce the model only after the operation and observation are understood.
- Begin with the problem and an intuitive model before introducing formal terminology.
- Prefer concrete examples, analogies, and small thought experiments over equations.
- Introduce formulas only when they are necessary for an accurate explanation or engineering estimate, and translate every symbol into plain language.
- Do not require the learner to pre-read an entire paper. Assign only the small section or figure needed for the current lesson.
- Correct misconceptions precisely without turning the lesson into a physics or mathematics survey.

## Visual Learning Rule

- When geometry, hierarchy, data flow, state transition, timing, or a multi-step protocol would be materially easier to understand visually, create a visual artifact instead of relying on prose alone.
- Choose the format that best serves the explanation. Mermaid is suitable for flows and relationships; SVG, PNG, Draw.io, or another format may be used for spatial layouts and more concrete illustrations. There is no preferred format.
- A visual must have a specific teaching purpose, readable labels, and an explanation of what the learner should notice. Do not create decorative diagrams.
- Store reusable visuals with the corresponding stage notes and link them from the note. Prefer editable or reproducible sources when practical.
- Verify that stored visual links and labels are correct before marking a stage complete.

## Stage Lifecycle

- Follow the order and completion criteria in `ROADMAP.md`.
- A stage is complete only after the learner passes its teach-back or exercise checkpoint.
- On completion, write a standalone stage note, update the notes index and current progress, mark the Roadmap, verify the documentation, and sync the stage commit to GitHub.
- Keep learning notes focused on durable understanding rather than transcripts of the conversation.
- Name stage notes with a zero-padded stage number and a meaningful topic slug. A stage with one document may use `docs/learning/NN-topic-name.md`. A stage with multiple documents must use `docs/learning/NN-topic-name/`, with `README.md` as the stage entry point and stage-specific supplementary documents and visual assets kept in that directory.
