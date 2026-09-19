"""Tests for literal guards, including explicit examples of their limitations."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_integrity import check, fenced_blocks, validate_manifest


class IntegrityTests(unittest.TestCase):
    def test_unchanged(self):
        self.assertEqual(check('Ready.', 'Ready.')['status'], 'pass')

    def test_missing_exact(self):
        self.assertEqual(check('Aruna uses CSV.', 'Uses CSV.', {'exact': ['Aruna']})['status'], 'fail')

    def test_exact_absent_from_source(self):
        with self.assertRaises(ValueError):
            check('Aruna.', 'Aruna.', {'exact': ['Invented']})

    def test_repeated_placeholder(self):
        result = check('{name}, confirm {name}.', '{name}, confirm.')
        self.assertEqual(result['hard_failures'][0]['missing'], {'{name}': 1})

    def test_placeholder_forms_in_translation(self):
        tokens = '{{count}} ${total} {name} {0} %s %1$s %(name)s'
        self.assertEqual(check('Save ' + tokens, 'Simpan ' + tokens)['status'], 'pass')

    def test_added_placeholder(self):
        self.assertEqual(check('Save.', 'Save {name}.')['status'], 'fail')

    def test_numeric_change_is_review(self):
        self.assertEqual(check('18%', '28%')['status'], 'review')

    def test_number_localization_is_review(self):
        self.assertEqual(check('1,250.50', '1.250,50')['status'], 'review')

    def test_code_change(self):
        a = '```python\nprint(1)\n```'
        b = '```python\nprint(2)\n```'
        self.assertEqual(check(a, b)['status'], 'fail')

    def test_translate_prose_not_code(self):
        code = '\n```python\nprint(1)\n```\n'
        self.assertEqual(check('Example' + code, 'Contoh' + code)['status'], 'pass')

    def test_long_fence_with_inner_short_fence(self):
        value = '````text\n```\nbody\n```\n````'
        self.assertEqual(fenced_blocks(value), [value])

    def test_tilde_fence(self):
        value = '~~~text\nabc\n~~~'
        self.assertEqual(fenced_blocks(value), [value])

    def test_disabled_code_guard(self):
        self.assertEqual(check('```\na\n```', '```\nb\n```', {'check_fenced_code': False})['status'], 'pass')

    def test_exact_count(self):
        self.assertEqual(check('Aruna Aruna', 'Aruna', {'counts': {'Aruna': 2}})['status'], 'fail')

    def test_source_count_error(self):
        with self.assertRaises(ValueError):
            check('Aruna', 'Aruna', {'counts': {'Aruna': 2}})

    def test_forbidden_literal(self):
        self.assertEqual(check('Fast.', 'Guaranteed.', {'forbidden': ['Guaranteed']})['status'], 'fail')

    def test_unknown_key(self):
        with self.assertRaises(ValueError):
            validate_manifest({'excat': ['Aruna']})

    def test_invalid_manifest_types(self):
        for value in ([], {'exact': 'Aruna'}, {'counts': {'x': True}}, {'check_numbers': 'yes'}, {'forbidden': ['']}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_manifest(value)

    def test_json_key_not_placeholder(self):
        self.assertEqual(check('{"label":"Save"}', '{"label":"Simpan"}')['status'], 'pass')

    def test_semantic_limitation_explicit(self):
        # This is deliberately a pass: literal guards cannot evaluate modality.
        self.assertEqual(check('You may leave.', 'You must leave.')['status'], 'pass')

    def test_units_limitation_explicit(self):
        # A semantic or configured exact-literal review must catch this change.
        self.assertEqual(check('Use 5 mg.', 'Use 5 g.')['status'], 'pass')

    def test_unicode(self):
        text = '\u4fdd\u5b58 {name}: 18%'
        self.assertEqual(check(text, text)['status'], 'pass')


if __name__ == '__main__':
    unittest.main()
