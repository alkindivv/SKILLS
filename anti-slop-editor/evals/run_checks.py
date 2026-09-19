#!/usr/bin/env python3
"""Run reproducible local checks, not a model-quality benchmark. Python 3.10+."""
from __future__ import annotations
import argparse
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_integrity import check


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional local JSON report path.')
    args = parser.parse_args()
    results: dict = {'kind': 'Deterministic local checks, not an LLM benchmark', 'python': sys.version.split()[0]}
    try:
        stream = io.StringIO()
        suite = unittest.defaultTestLoader.discover(str(ROOT / 'evals'), pattern='test_*.py')
        unit = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
        results['unit_tests'] = {'run': unit.testsRun, 'failures': len(unit.failures), 'errors': len(unit.errors), 'passed': unit.wasSuccessful()}
        if not unit.wasSuccessful():
            raise AssertionError(stream.getvalue())
        examples = json.loads((ROOT / 'evals/worked-examples.json').read_text())
        literal_pairs = 0
        for example in examples:
            before, after, rules = example['before'], example['after'], example['checks']
            name = example['id']
            for item in rules.get('required', []):
                assert item in after, (name, 'missing required text', item)
            for item in rules.get('forbidden', []):
                assert item not in after, (name, 'forbidden text', item)
            if rules.get('unchanged'):
                assert before == after, (name, 'unnecessary edit')
            if 'word_count' in rules:
                assert len(after.split()) == rules['word_count'], (name, 'word count')
            if 'json_keys' in rules:
                obj = json.loads(after)
                assert list(obj) == rules['json_keys'], (name, 'JSON keys')
            if rules.get('literal_check'):
                outcome = check(before, after, rules.get('manifest'))
                assert outcome['status'] == 'pass', (name, outcome)
                literal_pairs += 1
        assert (126 - 120) / 120 * 100 == 5.0
        results['worked_example_constraints'] = {'examples': len(examples), 'literal_pairs': literal_pairs, 'passed': True, 'semantic_certification': False}
        cases = json.loads((ROOT / 'evals/cases.json').read_text())['cases']
        assert len({c['id'] for c in cases}) == len(cases)
        assert all(c['prompt'] and c['expected'] and c['prohibited'] for c in cases)
        results['regression_prompts'] = {'count': len(cases), 'schema_checked': True, 'model_runs_performed': False}
        links = 0
        for path in ROOT.rglob('*.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
                if re.match(r'^[a-zA-Z]+:', target) or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                assert (path.parent / target).is_file(), ('broken local link', str(path), target)
                links += 1
        assert len(list(ROOT.rglob('SKILL.md'))) == 1
        assert (ROOT / 'agents/openai.yaml').is_file()
        assert len((ROOT / 'SKILL.md').read_text().splitlines()) < 500
        sources = json.loads((ROOT / 'references/sources.json').read_text())['sources']
        assert len(sources) == len({s['id'] for s in sources}) == 16
        results['structure'] = {'entrypoints': 1, 'local_links_checked': links, 'source_records': len(sources), 'passed': True}
        smoke = []
        with tempfile.TemporaryDirectory(prefix='anti-slop-check-') as tmp:
            directory = Path(tmp)
            source, target, manifest = [directory / x for x in ('source.txt', 'target.txt', 'manifest.json')]
            for label, before, after, config, expected_code, expected_status in [
                ('pass', 'Save {name}: 18%', 'Simpan {name}: 18%', {}, 0, 'pass'),
                ('review', '18%', '20%', {}, 0, 'review'),
                ('failure', 'Save {name}', 'Simpan', {}, 1, 'fail'),
                ('invalid-input', 'Ready', 'Ready', {'unknown': True}, 2, 'input_error'),
            ]:
                source.write_text(before, encoding='utf-8')
                target.write_text(after, encoding='utf-8')
                manifest.write_text(json.dumps(config), encoding='utf-8')
                proc = subprocess.run([sys.executable, str(ROOT / 'scripts/check_integrity.py'), '--source', str(source), '--target', str(target), '--manifest', str(manifest)], capture_output=True, text=True, timeout=15)
                payload = json.loads(proc.stdout)
                assert proc.returncode == expected_code and payload['status'] == expected_status, (label, proc.returncode, payload)
                smoke.append({'case': label, 'exit_code': proc.returncode, 'status': payload['status'], 'passed': True})
        results['cli_smoke_tests'] = smoke
        results['status'] = 'pass'
    except (AssertionError, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        results['status'] = 'fail'
        results['error'] = str(exc)
    rendered = json.dumps(results, ensure_ascii=False, indent=2) + '\n'
    print(rendered, end='')
    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
    return 0 if results['status'] == 'pass' else 1


if __name__ == '__main__':
    sys.exit(main())
