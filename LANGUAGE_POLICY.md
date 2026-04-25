# Language Policy / Языковая политика

## General Rules

- **Russian (RU)** — default language for clinical content: symptomatology, syndromology, pharmacotherapy, scales, oncopsychiatry, military psychiatry, nosologies, neurobiology.
- **Ukrainian (UA)** — mandatory for legal entries (category "Юридический статус (Украина)"), official document templates, references to Ukrainian legislation.

## Detailed Guidelines

| Area | Language | Reason |
|------|----------|--------|
| Category names | RU | UI identifiers, consistency across app |
| Clinical descriptions | RU | Shared post-Soviet medical education tradition |
| Legal entries (laws, orders) | UA | Must reference Ukrainian-language originals |
| Document templates (form 003/o etc.) | UA | Official forms are in Ukrainian |
| Scales (PHQ-9, GAD-7, AUDIT, CIWA) | RU or UA | Depends on validated translation used |
| Tags | Match entry language | For search consistency |
| Drug names | International (Latin-based) or RU | Per clinical convention |

## Rules

1. Do NOT mix RU and UA within a single `content` / `tactic` / `desc` field, unless quoting legislation or official documents.
2. When adding a new legal entry, use Ukrainian.
3. When adding a new clinical entry, use Russian.
4. Quoted legislation (e.g., "ст.14 ЗУ «Про психіатричну допомогу»") may appear in Ukrainian within Russian-language entries — this is acceptable.
