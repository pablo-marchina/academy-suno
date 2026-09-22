from __future__ import annotations
import unittest
from experiments.provider_compare_w004 import run_t007_a05 as mod


class T007A05Tests(unittest.TestCase):
    def test_population_models_and_bilingual_guardrails(self):
        tasks = mod.load_tasks()
        self.assertEqual(len(tasks), 4)
        self.assertEqual(mod.MODELS, ('openai/gpt-oss-120b', 'openai/gpt-oss-20b'))
        focus = next(t for t in tasks if t['source_id'] == 'bcb_focus_2026_08_21')
        self.assertIn(['expectativ', 'expectat'], focus['concept_groups'])
        copom = next(t for t in tasks if t['source_id'] == 'copom_277_2026_03')
        self.assertIn(['restritiv', 'restrictiv'], copom['concept_groups'])

    def test_all_four_raw_source_contexts_self_validate(self):
        for task in mod.load_tasks():
            source_text = ' '.join(task['anchors'] + task['qualifiers'])
            q = mod.validate_output(task, {
                'summary_ptbr': source_text,
                'qualifier_copy': task['qualifiers'],
                'caveat_ptbr': ' '.join(task['qualifiers']) or 'Sem qualifier adicional.',
            })
            self.assertEqual(q['numeric_recall'], 1.0, task['source_id'])
            self.assertEqual(q['concept_recall'], 1.0, task['source_id'])
            self.assertTrue(q['exact_qualifier_copy'], task['source_id'])
            self.assertTrue(q['no_unsupported_numeric_facts'], task['source_id'])
            self.assertTrue(q['preservation_pass'], task['source_id'])

    def test_short_auditable_response_shape_and_limit(self):
        p = mod.prompt(mod.load_tasks()[0])
        self.assertIn('summary_ptbr', p)
        self.assertIn('qualifier_copy', p)
        self.assertIn('caveat_ptbr', p)
        self.assertEqual(mod.MAX_OUTPUT_TOKENS, 1536)

    def test_checker_rejects_invented_number(self):
        task = mod.load_tasks()[0]
        q = mod.validate_output(task, {
            'summary_ptbr': 'Selic IPCA restrictive 999999999',
            'qualifier_copy': task['qualifiers'],
            'caveat_ptbr': ' '.join(task['qualifiers']) or 'Cuidado.',
        })
        self.assertFalse(q['no_unsupported_numeric_facts'])
        self.assertFalse(q['preservation_pass'])

    def test_a03_validation_labels_are_not_quality_gold(self):
        self.assertNotIn('model_validation_a03', mod.prompt(mod.load_tasks()[0]))


if __name__ == '__main__':
    unittest.main()
