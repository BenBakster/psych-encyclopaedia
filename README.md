# PSYCH :: ENCYCLOPAEDIA OS

Source-of-truth для PSYCH :: ENCYCLOPAEDIA OS — клинической справочной базы по психиатрии и наркологии (RU/UA, ~124 entries в 20 категориях).

**Live demo:** https://benbakster.github.io/psych-encyclopaedia/

---

## ⚠ Дисклеймер

Этот репозиторий — **образовательный ресурс для практикующих врачей-психиатров и наркологов**. Не клиническая рекомендация, не замена клинического суждения, не справочник для самолечения пациентами.

Локальные законы, формуляры и клинические гайдлайны могут отличаться. Всегда сверяйся с первоисточниками (указаны в `sources[]` каждой записи) и применяй суждение, адекватное юрисдикции и пациенту.

Автор не несёт ответственности за последствия использования.

---

## Структура

```
categories/        — JSON source files, по одному на категорию (20 файлов)
build.py           — собирает все JSON, валидирует, пишет в database.js
schema.js          — JSDoc типы (для редактора, не runtime)
LANGUAGE_POLICY.md — правила использования RU/UA в content
docs/              — output для GitHub Pages: index.html + database.js
wiki/              — внутренняя документация (BRIEF, гайдлайны)
.github/           — CI workflow + issue templates + Codespace devcontainer
```

## Build

```bash
python3 build.py           # обычный build
python3 build.py --strict  # warnings = errors (рекомендуемо)
```

Output: `docs/database.js` (для Pages) + `$PSYCH_RENDERER_DIR/database.js` (для локального renderer).

## Workflow для контрибуции

1. Создать ветку: `git checkout -b feature/<name>`
2. Редактировать `categories/*.json` (никогда не `database.js` — он автогенерируется)
3. Запустить `python3 build.py` — обновляет docs/ + локальный renderer
4. Открыть `terminal1.html` (или https://benbakster.github.io/psych-encyclopaedia/), проверить визуально
5. Commit + push, открыть PR в `main`
6. CI прогоняет `--strict` валидацию + проверку графов flowchart-ов
7. После зелёного статуса — `gh pr merge <N> --merge`

Direct push в `main` заблокирован branch protection.

## Лицензия

[CC BY-NC-ND 4.0](LICENSE) — Attribution, NonCommercial, NoDerivatives.

Коммерческое использование, форки и derivative works — **только с письменного разрешения автора**.

## Автор

Anton Vilenchyk (Антон Віленчик), MD — психиатр-нарколог, Київ, Україна.

Bogomolets National Medical University (2010–2017). NEI Master of Psychopharmacology (2020, 2021 with distinction).

Контакт: [@ben.bakster](https://instagram.com/ben.bakster) · GitHub: [@BenBakster](https://github.com/BenBakster)

## Источники

См. [`wiki/BRIEF-pharm-flowcharts.md`](wiki/BRIEF-pharm-flowcharts.md) §1.5 — иерархия источников по приоритету (Maudsley, Stahl, Bazire, NEUROP/Riederer-Laux, NICE/CANMAT/BAP/VA-DoD, Авруцкий/Воронков/Чуприков, ICD-10/DSM-5-TR).

## Related repos

- [`krok2-trainer`](https://github.com/BenBakster/krok2-trainer) — тренажёр по КРОК-2
- [`psych-qbank`](https://github.com/BenBakster/psych-qbank) — UWorld-style q-bank
- [`ampd-tools`](https://github.com/BenBakster/ampd-tools) — AMPD/PID-5 инструменты
- [`pid5-irf`](https://github.com/BenBakster/pid5-irf) — PID-5 informant report
