# AGENTS.md

This file applies to the whole repository.

## Project Scope

`psych-encyclopaedia` is a clinical reference and educational knowledge base for practicing psychiatrists and narcologists. Treat clinical accuracy, source traceability, language consistency, and safety disclaimers as core product behavior.

## Clinical Safety

- Do not present repository content as a substitute for clinical judgment, formal guidelines, local law, or emergency care.
- Preserve existing disclaimers and make new patient-facing or public-facing text equally conservative.
- Avoid diagnostic certainty, treatment guarantees, or instructions for self-treatment.
- When adding or changing clinical claims, keep them tied to explicit `sources[]` entries or repository source hierarchy.
- Flag unclear, outdated, conflicting, or jurisdiction-sensitive medical content instead of silently normalizing it.

## Source Of Truth

- Edit `categories/*.json` for knowledge-base content.
- Do not manually edit generated `docs/database.js` except when the task explicitly targets generated output inspection.
- Run the build after content changes so generated files stay aligned.
- Follow `LANGUAGE_POLICY.md` for RU/UA content and terminology.
- Check `wiki/` for editorial rules, flowchart conventions, and source hierarchy before broad content edits.

## Development Workflow

- Before editing, inspect `README.md`, `LANGUAGE_POLICY.md`, relevant `wiki/` notes, and nearby category examples.
- Keep changes small and content-focused. Do not combine clinical content changes with UI, build, or formatting churn unless required.
- Preserve existing JSON structure, identifiers, field names, and ordering conventions unless the task is a schema migration.
- For flowcharts, verify node references, decision paths, and terminal outcomes after edits.
- Keep public GitHub Pages output functional and static; do not introduce server-side storage, tracking, or patient-data collection without explicit approval.

## Validation

For content or schema changes, run the narrowest relevant check available:

```bash
python3 build.py
python3 build.py --strict
```

If Python is invoked as `python` on the current machine, use the local equivalent. Report any validation that could not be run.

## Review Focus

When reviewing changes, prioritize:

- broken JSON or schema drift;
- generated output out of sync with sources;
- unsupported clinical claims;
- missing or weak citations;
- RU/UA terminology inconsistency;
- unsafe public-facing wording;
- broken flowchart edges or unreachable outcomes;
- accidental edits to generated files.

## Codex Behavior

- Answer in the user's language unless repository text requires RU/UA/EN matching.
- Be concise, but include enough evidence for clinical or source-sensitive changes.
- Ask before adding new external dependencies, analytics, backend services, or anything that could collect identifiable patient data.
