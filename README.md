# PSYCH_DATABASE — Source Files

## Structure

```
database/
  build.py           — Build script: validates JSONs, outputs database.js
  migrate.py         — One-time migration from old monolithic database.js
  schema.js          — JSDoc type definitions (not loaded at runtime)
  LANGUAGE_POLICY.md — RU/UA language rules
  README.md          — This file
  categories/        — JSON source files, one per category
    urgetnaya-psihiatriya.json
    simptomatologiya.json
    ...
```

## Workflow

### Edit data
1. Edit the relevant JSON file in `categories/`
2. Update `lastUpdated` field to today's date
3. Add sources to `sources` array if applicable

### Build
```bash
python database/build.py
```
This reads all JSON files, validates them, and writes `../database.js`.

### Validation
The build script checks:
- **Errors** (block build): duplicate IDs, duplicate cmd_alias, missing fields, invalid type, missing type-specific data
- **Warnings** (reported): broken `related` references, empty tags/sources

Use `--strict` flag to treat warnings as errors:
```bash
python database/build.py --strict
```

### Add a new entry
1. Open the relevant category JSON file
2. Add a new object to the array (see schema.js for type definitions)
3. Set `lastUpdated` to today, `sources` to citations
4. Run `node database/build.js` to validate and build

### Add a new category
1. Create a new JSON file in `categories/` (use transliterated kebab-case name)
2. Add the category name to `CATEGORY_ORDER` array in `build.js`
3. Run build

## Output
The build writes to `../database.js` — the file loaded by `terminal.html` and `terminal1.html` via `<script src="database.js">`.

**Do NOT edit `database.js` directly** — it is auto-generated.
