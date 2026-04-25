#!/usr/bin/env python3
"""
build.py — Build script for PSYCH_DATABASE.

Reads all JSON files from categories/, validates them, and outputs
a single database.js file that the HTML app loads via <script> tag.

Usage:
    python build.py           # Normal build (warnings allowed)
    python build.py --strict  # Treat warnings as errors

Exit codes:
    0 — success
    1 — validation errors found
"""

import json
import os
import re
import sys
import io
from datetime import datetime

# Force UTF-8 stdout on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORIES_DIR = os.path.join(SCRIPT_DIR, 'categories')
# Output goes to the renderer folder where terminal1.html loads it via <script>.
# Override with PSYCH_RENDERER_DIR env var on other machines.
RENDERER_DIR = os.environ.get(
    'PSYCH_RENDERER_DIR',
    '/home/thx1138/Документи/Инструменты_HTML',
)
OUTPUT_FILES = [
    os.path.join(RENDERER_DIR, 'database.js'),
]

VALID_TYPES = {'matrix', 'text', 'table', 'flowchart', 'calculator', 'checklist'}

REQUIRED_FIELDS = {'id', 'cmd_alias', 'type', 'category', 'title', 'tags', 'related', 'lastUpdated', 'sources'}

# Type-specific required data fields
TYPE_DATA_FIELDS = {
    'matrix': 'matrix',
    'text': 'content',
    'table': 'tableHeaders',  # also tableRows, checked separately
    'flowchart': 'flowchart',
    'calculator': 'calculator',
    'checklist': 'checklist',
}

# Category display order (matches original database.js order)
CATEGORY_ORDER = [
    'Ургентная психиатрия',
    'Симптоматология',
    'Синдромология',
    'Фармакотерапия (АД)',
    'Фармакотерапия (Общее)',
    'Фармакотерапия (АП)',
    'Шкалы и Калькуляторы',
    'Психоонкология',
    'Военная психиатрия',
    'Юридический статус (Украина)',
    'Диагностические критерии (МКБ-10)',
    'Фармакотерапия (Нормотимики)',
    'Наркология',
    'Тревожные расстройства',
    'Аффективные расстройства',
    'Расстройства личности',
    'Расстройства сна',
    'Нейробиология (Stahl)',
    'Нейроразвитие',
    'Феноменология (Ясперс)',
]

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    @property
    def has_errors(self):
        return len(self.errors) > 0

    @property
    def has_warnings(self):
        return len(self.warnings) > 0

    def print_report(self):
        if self.errors:
            print(f'\n--- ERRORS ({len(self.errors)}) ---')
            for e in self.errors:
                print(f'  ERROR: {e}')

        if self.warnings:
            print(f'\n--- WARNINGS ({len(self.warnings)}) ---')
            for w in self.warnings:
                print(f'  WARN:  {w}')

        if not self.errors and not self.warnings:
            print('\n  Validation passed with no issues.')


def load_all_entries():
    """Load and combine all JSON files from categories/."""
    all_entries = []
    files_loaded = []

    if not os.path.isdir(CATEGORIES_DIR):
        print(f'ERROR: Categories directory not found: {CATEGORIES_DIR}')
        sys.exit(1)

    for filename in sorted(os.listdir(CATEGORIES_DIR)):
        if not filename.endswith('.json'):
            continue
        filepath = os.path.join(CATEGORIES_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                entries = json.load(f)
        except json.JSONDecodeError as e:
            print(f'ERROR: Invalid JSON in {filename}: {e}')
            sys.exit(1)

        if not isinstance(entries, list):
            print(f'ERROR: {filename} must contain a JSON array')
            sys.exit(1)

        all_entries.extend(entries)
        files_loaded.append((filename, len(entries)))

    return all_entries, files_loaded


def validate(entries):
    """Run all validation rules on the combined entry list."""
    v = ValidationResult()

    all_ids = set()
    all_aliases = set()
    id_set = set()

    # Collect all IDs first for related-ref checking
    for entry in entries:
        eid = entry.get('id', '')
        if eid:
            id_set.add(eid)

    for entry in entries:
        eid = entry.get('id', '<missing>')
        alias = entry.get('cmd_alias', '<missing>')
        etype = entry.get('type', '<missing>')
        category = entry.get('category', '<missing>')

        label = f'[{eid}]'

        # --- ERRORS ---

        # Required fields
        for field in REQUIRED_FIELDS:
            if field not in entry:
                v.error(f'{label} Missing required field: {field}')

        # Duplicate ID
        if eid in all_ids:
            v.error(f'{label} Duplicate id: "{eid}"')
        all_ids.add(eid)

        # Duplicate cmd_alias
        if alias in all_aliases:
            v.error(f'{label} Duplicate cmd_alias: "{alias}"')
        all_aliases.add(alias)

        # Invalid type
        if etype not in VALID_TYPES:
            v.error(f'{label} Invalid type: "{etype}" (allowed: {VALID_TYPES})')

        # Missing type-specific data
        if etype in TYPE_DATA_FIELDS:
            data_field = TYPE_DATA_FIELDS[etype]
            if data_field not in entry:
                v.error(f'{label} Type "{etype}" requires field "{data_field}"')

        # Table entries also need tableRows
        if etype == 'table' and 'tableRows' not in entry:
            v.error(f'{label} Type "table" requires field "tableRows"')

        # Date format
        last_updated = entry.get('lastUpdated', '')
        if last_updated and not DATE_RE.match(last_updated):
            v.error(f'{label} Invalid lastUpdated format: "{last_updated}" (expected YYYY-MM-DD)')

        # --- WARNINGS ---

        # Broken related references
        related = entry.get('related', [])
        if isinstance(related, list):
            for ref in related:
                if ref not in id_set:
                    v.warn(f'{label} Broken related reference: "{ref}"')

        # Empty tags
        tags = entry.get('tags', [])
        if isinstance(tags, list) and len(tags) == 0:
            v.warn(f'{label} Empty tags array')

        # Empty related
        if isinstance(related, list) and len(related) == 0:
            v.warn(f'{label} Empty related array')

        # Empty sources
        sources = entry.get('sources', [])
        if isinstance(sources, list) and len(sources) == 0:
            v.warn(f'{label} Empty sources array')

        # Unknown category
        if category not in CATEGORY_ORDER:
            v.warn(f'{label} Category "{category}" not in CATEGORY_ORDER')

    return v


def sort_entries(entries):
    """Sort entries by category order, preserving order within each category."""
    cat_index = {cat: i for i, cat in enumerate(CATEGORY_ORDER)}

    def sort_key(entry):
        cat = entry.get('category', '')
        return cat_index.get(cat, len(CATEGORY_ORDER))

    # Stable sort: preserves original order within same category
    return sorted(entries, key=sort_key)


def generate_output(entries):
    """Generate the database.js file content."""
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # Count categories
    categories = set(e.get('category', '') for e in entries)

    header = f"""// SYSTEM.CORE.DB v7.0 [ENCYCLOPAEDIA KERNEL]
// Auto-generated by build.py on {now}
// DO NOT EDIT — source files in database/categories/
// Entries: {len(entries)} | Categories: {len(categories)}

window.PSYCH_DATABASE = """

    body = json.dumps(entries, ensure_ascii=False, indent=2)

    return header + body + ';\n'


def main():
    strict = '--strict' in sys.argv

    print('=== PSYCH_DATABASE Build ===\n')

    # Load
    entries, files_loaded = load_all_entries()
    print(f'Loaded {len(entries)} entries from {len(files_loaded)} files:')
    for filename, count in files_loaded:
        print(f'  {filename}: {count}')

    # Validate
    print('\nValidating...')
    result = validate(entries)
    result.print_report()

    has_fatal = result.has_errors or (strict and result.has_warnings)

    if has_fatal:
        if strict and result.has_warnings and not result.has_errors:
            print('\n--strict mode: warnings treated as errors.')
        print(f'\nBuild FAILED. Fix the issues above.')
        sys.exit(1)

    # Sort
    entries = sort_entries(entries)

    # Generate output
    output = generate_output(entries)
    for output_file in OUTPUT_FILES:
        output_dir = os.path.dirname(output_file)
        if os.path.isdir(output_dir):
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f'\nWritten: {output_file}')

    print(f'\nBuild SUCCESS.')
    print(f'Size: {len(output.encode("utf-8")) / 1024:.1f} KB')
    print(f'Entries: {len(entries)}')

    # Summary stats
    type_counts = {}
    for e in entries:
        t = e.get('type', 'unknown')
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f'\nBy type: {type_counts}')

    sources_total = sum(len(e.get('sources', [])) for e in entries)
    print(f'Total citations in sources[]: {sources_total}')


if __name__ == '__main__':
    main()
