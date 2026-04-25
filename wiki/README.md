# PSYCH :: ENCYCLOPAEDIA OS — Wiki

База знаний практикующего психиатра-нарколога (Киев, Украина).

## Контент репозитория

- **Source-of-truth:** `categories/*.json` — 20 файлов по категориям, всего ~124 entries.
- **Build:** `python3 build.py` собирает в `database.js`.
- **Renderer:** `terminal1.html` (PSYCH :: ENCYCLOPAEDIA OS v7.1) — React + standalone.
- **Pages:** https://benbakster.github.io/psych-encyclopaedia/ (private — только collaborators видят).

## Документы Wiki

- [[BRIEF-pharm-flowcharts]] — задание для агента-ассистента: 5 фарма-flowchart-ов, правила работы с базой, формуляр.
- [[Language-Policy]] — RU/UA языковые правила для разных типов контента.
- [[Build-Pipeline]] — как работает `build.py`, schema, валидация.

## Типы записей (entries)

| Тип | Зачем | Примеры |
|---|---|---|
| `matrix` | Многомерный обзор: past/current/future + pheno/neuro/tactic | bipolar_overview, alcohol_dependency, alg_agitation |
| `text` | Простой контент с заголовком и markdown-style текстом | metalcohol_delirium, treatment_resistant_depression |
| `table` | Структурированные сравнения с headers + rows | ad_side_effects, pharma_receptors |
| `flowchart` | Wizard-навигация с ветвлениями (developments через `next:`) | alg_acute_agitation, alg_alcohol_withdrawal, flowchart_ad |
| `calculator` | Шкалы и эквиваленты (PHQ-9, CIWA, AUDIT, calc_cpz) | calc_phq9, calc_ciwa, calc_cpz |
| `checklist` | Чек-листы с секциями (мониторинг, готовность к процедуре) | clozapine_monitoring, ptsd_checklist |

## Категории (20)

Ургентная психиатрия · Симптоматология · Синдромология · Фармакотерапия (АД) · Фармакотерапия (Общее) · Фармакотерапия (АП) · Шкалы и Калькуляторы · Психоонкология · Военная психиатрия · Юридический статус (Украина) · Диагностические критерии (МКБ-10) · Фармакотерапия (Нормотимики) · Наркология · Тревожные расстройства · Аффективные расстройства · Расстройства личности · Расстройства сна · Нейробиология (Stahl) · Нейроразвитие · Феноменология (Ясперс)

## Контрибуция

Issues — для тех-долга, багов, feature requests. Шаблоны: `bug_report`, `feature_request`, `empty_sources`.

PR — каждый flowchart/entry отдельным коммитом, source files в `categories/`, не в `database.js` напрямую.

## Источники (по приоритету для новых записей)

См. `BRIEF §1.5`. Кратко:
1. Maudsley Prescribing Guidelines
2. Stahl Essential Psychopharmacology + Prescriber's Guide
3. Schatzberg & Nemeroff
4. NEI / Master Psychopharmacology
5. Bazire (Psychotropic Drug Directory)
6. **NEUROP / Riederer-Laux 2022** (расширено в работе апр.2026)
7. Профильные guidelines: APA, NICE, CINP, WFSBP, CANMAT
8. Постсоветская: Авруцкий, Воронков, Чуприков
9. Украинские: наказы МОЗ, ЗУ «Про психіатричну допомогу»
