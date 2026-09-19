#!/usr/bin/env python3
"""Advisory literal-integrity checks. Not an AI detector or semantic verifier.

Exit codes: 0 = pass or review flags, 1 = configured hard failure, 2 = invalid
input. Always read the JSON status. No network calls and no file writes.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
from typing import Any

MAX_BYTES = 10 * 1024 * 1024
PLACEHOLDER = re.compile(
    r"\{\{[^{}\n]+\}\}|\$\{[A-Za-z_][\w.]*\}|"
    r"\{(?:[A-Za-z_][\w.]*|\d+)\}|"
    r"(?<!%)%(?:\d+\$)?[sdif]|(?<!%)%\([A-Za-z_]\w*\)[sdif]"
)
NUMBER = re.compile(r"(?<![\w])[-+]?\d+(?:[.,]\d+)*(?:%|\u2030)?")
FENCE_START = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})[^\r\n]*$")
ALLOWED_KEYS = {
    'exact', 'counts', 'forbidden', 'check_placeholders',
    'check_fenced_code', 'check_numbers'
}
LIMITS = [
    'No semantic, factual, stylistic, or authorship assessment.',
    'Numbers are surface tokens; locale changes and authorized omissions need review.',
    'Placeholder recognition is limited; ICU, HTML, JSON, and YAML need proper parsers.',
    'No automatic extraction of all names, quotations, links, units, or negation.'
]


def read_text(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f'Not a regular file: {path}')
    if path.stat().st_size > MAX_BYTES:
        raise ValueError(f'File exceeds {MAX_BYTES} bytes: {path}')
    return path.read_text(encoding='utf-8')


def validate_manifest(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError('Manifest must be a JSON object.')
    unknown = set(value) - ALLOWED_KEYS
    if unknown:
        raise ValueError('Unknown manifest keys: ' + ', '.join(sorted(unknown)))
    for key in ('exact', 'forbidden'):
        items = value.get(key, [])
        if not isinstance(items, list) or any(
            not isinstance(item, str) or not item for item in items
        ):
            raise ValueError(f'{key} must be a list of non-empty strings.')
    counts = value.get('counts', {})
    if not isinstance(counts, dict) or any(
        not isinstance(k, str) or not k or type(v) is not int or v < 0
        for k, v in counts.items()
    ):
        raise ValueError('counts must map non-empty strings to nonnegative integers.')
    for key in ('check_placeholders', 'check_fenced_code', 'check_numbers'):
        if key in value and not isinstance(value[key], bool):
            raise ValueError(f'{key} must be a boolean.')
    return value


def fenced_blocks(text: str) -> list[str]:
    """Collect ordinary Markdown fences; not a full Markdown parser."""
    blocks: list[str] = []
    current: list[str] = []
    closing: re.Pattern[str] | None = None
    for line in text.splitlines(keepends=True):
        bare = line.rstrip('\r\n')
        if closing is None:
            start = FENCE_START.match(bare)
            if start:
                marker = start.group(1)
                closing = re.compile(
                    r'^[ ]{0,3}' + re.escape(marker[0]) +
                    '{' + str(len(marker)) + r',}[ \t]*$'
                )
                current = [line]
        else:
            current.append(line)
            if closing.match(bare):
                blocks.append(''.join(current).rstrip('\r\n'))
                current = []
                closing = None
    if current:
        blocks.append(''.join(current).rstrip('\r\n'))
    return blocks


def difference(before: Counter[str], after: Counter[str]) -> dict[str, Any]:
    return {
        'missing': dict(sorted((before - after).items())),
        'added': dict(sorted((after - before).items())),
    }


def check(source: str, target: str, manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    config = validate_manifest({} if manifest is None else manifest)
    failures: list[dict[str, Any]] = []
    flags: list[dict[str, Any]] = []
    for literal in config.get('exact', []):
        if literal not in source:
            raise ValueError(f'Protected literal is absent from source: {literal!r}')
        if literal not in target:
            failures.append({'check': 'exact_literal_missing', 'literal': literal})
    for literal, expected in config.get('counts', {}).items():
        actual_source = source.count(literal)
        if actual_source != expected:
            raise ValueError(
                f'Source count for {literal!r} is {actual_source}, not {expected}.'
            )
        actual_target = target.count(literal)
        if actual_target != expected:
            failures.append({
                'check': 'literal_count_changed', 'literal': literal,
                'expected': expected, 'actual': actual_target
            })
    for literal in config.get('forbidden', []):
        if literal in target:
            failures.append({'check': 'forbidden_literal_present', 'literal': literal})
    if config.get('check_placeholders', True):
        before = Counter(PLACEHOLDER.findall(source))
        after = Counter(PLACEHOLDER.findall(target))
        if before != after:
            failures.append({'check': 'placeholders_changed', **difference(before, after)})
    if config.get('check_fenced_code', True):
        before_blocks, after_blocks = fenced_blocks(source), fenced_blocks(target)
        if before_blocks != after_blocks:
            failures.append({
                'check': 'fenced_code_changed',
                'source_block_count': len(before_blocks),
                'target_block_count': len(after_blocks)
            })
    if config.get('check_numbers', True):
        before_n, after_n = Counter(NUMBER.findall(source)), Counter(NUMBER.findall(target))
        if before_n != after_n:
            flags.append({'check': 'numeric_tokens_changed', **difference(before_n, after_n)})
    status = 'fail' if failures else ('review' if flags else 'pass')
    return {'status': status, 'hard_failures': failures, 'review_flags': flags, 'limits': LIMITS}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--source', type=Path, required=True, help='Original UTF-8 text file.')
    parser.add_argument('--target', type=Path, required=True, help='Revised UTF-8 text file.')
    parser.add_argument('--manifest', type=Path, help='Optional JSON literal-preservation manifest.')
    args = parser.parse_args(argv)
    try:
        source, target = read_text(args.source), read_text(args.target)
        manifest = json.loads(read_text(args.manifest)) if args.manifest else {}
        result = check(source, target, manifest)
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({'status': 'input_error', 'error': str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['hard_failures'] else 0


if __name__ == '__main__':
    sys.exit(main())
