#!/usr/bin/env python3
"""
migrate.py — One-time migration from monolithic database.js to JSON modules.

Reads the original database.js, splits entries by category,
adds lastUpdated and sources fields, writes JSON files to categories/.

Usage: python migrate.py
"""

import json
import os
import re
import sys
import io

# Force UTF-8 stdout on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(SCRIPT_DIR, '..', 'database.js')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'categories')

CATEGORY_TO_FILE = {
    'Ургентная психиатрия': 'urgetnaya-psihiatriya.json',
    'Симптоматология': 'simptomatologiya.json',
    'Синдромология': 'sindromologiya.json',
    'Фармакотерапия (АД)': 'farmakoterapiya-ad.json',
    'Фармакотерапия (АП)': 'farmakoterapiya-ap.json',
    'Фармакотерапия (Нормотимики)': 'farmakoterapiya-normotimiki.json',
    'Фармакотерапия (Общее)': 'farmakoterapiya-obshchee.json',
    'Шкалы и Калькуляторы': 'shkaly-i-kalkulyatory.json',
    'Психоонкология': 'psihoonkologiya.json',
    'Военная психиатрия': 'voennaya-psihiatriya.json',
    'Юридический статус (Украина)': 'yuridicheskiy-status-ukraina.json',
    'Диагностические критерии (МКБ-10)': 'diagnosticheskie-kriterii-mkb10.json',
    'Наркология': 'narkologiya.json',
    'Тревожные расстройства': 'trevozhnye-rasstroystva.json',
    'Аффективные расстройства': 'affektivnye-rasstroystva.json',
    'Расстройства личности': 'rasstroystva-lichnosti.json',
    'Расстройства сна': 'rasstroystva-sna.json',
    'Нейробиология (Stahl)': 'neyrobiologiya-stahl.json',
    'Нейроразвитие': 'neyrorazvitie.json',
}

CITATION_PATTERNS = [
    r'По\s+([A-Za-zА-Яа-яёЁіІїЇєЄґҐ\s&,.\'-]+?\s*\(\d{4}\))',
    r'по\s+([A-Za-zА-Яа-яёЁіІїЇєЄґҐ\s&,.\'-]+?\s*\(\d{4}\))',
    r'([A-Z][a-z]+(?:\s+(?:et\s+al\.|&\s+[A-Z][a-z]+))?(?:\s*\(\d{4}\)))',
]


def transliterate(category):
    translit = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'і': 'i', 'ї': 'yi', 'є': 'ye', 'ґ': 'g',
    }
    result = []
    for c in category.lower():
        result.append(translit.get(c, c))
    text = ''.join(result)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text + '.json'


def extract_citations(entry):
    sources = set()
    text_fields = [
        entry.get('description', ''),
        entry.get('content', ''),
    ]
    matrix = entry.get('matrix', {})
    if isinstance(matrix, dict):
        current = matrix.get('current', {})
        if isinstance(current, dict):
            for key in ('tactic', 'pheno', 'neuro'):
                text_fields.append(current.get(key, ''))

    for text in text_fields:
        if not isinstance(text, str):
            continue
        for pattern in CITATION_PATTERNS:
            for match in re.finditer(pattern, text):
                citation = match.group(1).strip()
                if 10 < len(citation) < 200:
                    sources.add(citation)
    return sorted(sources)


def js_to_json(js_source):
    """Convert JavaScript object literal array to valid JSON.

    Character-by-character parser that properly handles:
    - Single-line comments (// ...) outside strings
    - Unquoted object keys
    - Trailing commas
    - String escapes
    """
    # Phase 1: Strip comments, preserving string contents
    buf = []
    i = 0
    n = len(js_source)
    in_str = False
    str_ch = None

    while i < n:
        c = js_source[i]

        if in_str:
            buf.append(c)
            if c == '\\' and i + 1 < n:
                buf.append(js_source[i + 1])
                i += 2
                continue
            if c == str_ch:
                in_str = False
            i += 1
            continue

        if c in ('"',):
            in_str = True
            str_ch = c
            buf.append(c)
            i += 1
            continue

        # JS single-quoted strings — convert to double-quoted
        if c == "'":
            in_str = True
            str_ch = "'"
            buf.append('"')  # Replace opening ' with "
            i += 1
            # Read until closing ', converting inner escapes
            while i < n:
                cc = js_source[i]
                if cc == '\\' and i + 1 < n:
                    buf.append(cc)
                    buf.append(js_source[i + 1])
                    i += 2
                    continue
                if cc == "'":
                    buf.append('"')  # Replace closing ' with "
                    i += 1
                    in_str = False
                    break
                if cc == '"':
                    buf.append('\\"')  # Escape inner double quotes
                    i += 1
                    continue
                buf.append(cc)
                i += 1
            continue

        if c == '/' and i + 1 < n and js_source[i + 1] == '/':
            while i < n and js_source[i] != '\n':
                i += 1
            continue

        if c == '/' and i + 1 < n and js_source[i + 1] == '*':
            i += 2
            while i < n - 1 and not (js_source[i] == '*' and js_source[i + 1] == '/'):
                i += 1
            i += 2
            continue

        buf.append(c)
        i += 1

    cleaned = ''.join(buf)

    # Phase 2: Extract the array
    start = cleaned.find('window.PSYCH_DATABASE')
    if start == -1:
        raise ValueError("Could not find window.PSYCH_DATABASE")
    eq = cleaned.find('=', start)
    arr_start = cleaned.find('[', eq)
    arr_end = cleaned.rfind(']')
    if arr_start == -1 or arr_end == -1:
        raise ValueError("Could not find array brackets")

    content = cleaned[arr_start:arr_end + 1]

    # Phase 3: Quote unquoted keys (character-by-character, outside strings)
    result = []
    i = 0
    n = len(content)
    in_str = False

    while i < n:
        c = content[i]

        if in_str:
            result.append(c)
            if c == '\\' and i + 1 < n:
                result.append(content[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue

        if c == '"':
            in_str = True
            result.append(c)
            i += 1
            continue

        # Check for unquoted key: a word followed by :
        if c.isalpha() or c == '_':
            # Collect the word
            word_start = i
            while i < n and (content[i].isalnum() or content[i] == '_'):
                i += 1
            word = content[word_start:i]

            # Skip whitespace
            j = i
            while j < n and content[j] in (' ', '\t'):
                j += 1

            if j < n and content[j] == ':':
                # This is an unquoted key — quote it
                result.append('"')
                result.append(word)
                result.append('"')
            else:
                # Not a key — check for JS literals
                if word == 'true':
                    result.append('true')
                elif word == 'false':
                    result.append('false')
                elif word == 'null':
                    result.append('null')
                else:
                    result.append(word)
            continue

        result.append(c)
        i += 1

    content = ''.join(result)

    # Phase 4: Remove trailing commas
    content = re.sub(r',(\s*[}\]])', r'\1', content)

    return content


def main():
    print('=== PSYCH_DATABASE Migration ===\n')

    if not os.path.exists(SOURCE_FILE):
        print(f'ERROR: Source file not found: {SOURCE_FILE}')
        sys.exit(1)

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        source = f.read()

    print('Parsing database.js...')
    try:
        json_str = js_to_json(source)
        db = json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        print(f'ERROR: Failed to parse database.js: {e}')
        if isinstance(e, json.JSONDecodeError):
            # Show context around error
            lines = json_str.split('\n')
            line_num = e.lineno - 1
            start_line = max(0, line_num - 2)
            end_line = min(len(lines), line_num + 3)
            for li in range(start_line, end_line):
                marker = '>>>' if li == line_num else '   '
                print(f'  {marker} {li+1}: {lines[li][:120]}')
        sys.exit(1)

    if not isinstance(db, list) or len(db) == 0:
        print('ERROR: Parsed result is not a non-empty array')
        sys.exit(1)

    print(f'Loaded {len(db)} entries from database.js\n')

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Group by category
    groups = {}
    for entry in db:
        cat = entry.get('category', 'UNKNOWN')
        if cat not in groups:
            groups[cat] = []
        entry['lastUpdated'] = '2026-04-03'
        entry['sources'] = extract_citations(entry)
        groups[cat].append(entry)

    # Write JSON files
    total_entries = 0
    for category, entries in groups.items():
        filename = CATEGORY_TO_FILE.get(category)
        if not filename:
            filename = transliterate(category)
            print(f'  WARNING: Unknown category "{category}" -> {filename}')

        output_path = os.path.join(OUTPUT_DIR, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)

        total_entries += len(entries)
        print(f'  {filename}: {len(entries)} entries')

    print(f'\n=== Migration Complete ===')
    print(f'Total entries: {total_entries}')
    print(f'Categories: {len(groups)}')
    print(f'Output directory: {OUTPUT_DIR}')

    citation_count = sum(
        len(e['sources']) for entries in groups.values() for e in entries
    )
    print(f'Extracted {citation_count} citations into sources[] fields.')


if __name__ == '__main__':
    main()
