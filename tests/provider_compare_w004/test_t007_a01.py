from __future__ import annotations
import unittest
from experiments.provider_compare_w004 import run_t007_a01 as mod


class T007A01Tests(unittest.TestCase):
    def test_task_population_is_four_development_sources(self):
        tasks=mod.load_tasks()
        self.assertEqual(len(tasks),4)
        self.assertEqual(len({t['source_id'] for t in tasks}),4)
        self.assertTrue(all(t['anchors'] for t in tasks))

    def test_prompt_requires_identical_auditable_shape(self):
        p=mod.prompt(mod.load_tasks()[0])
        self.assertIn('evidence_copy',p)
        self.assertIn('qualifier_copy',p)
        self.assertIn('summary_ptbr',p)
        self.assertIn('add no numeric facts',p)

    def test_quality_checker_rewards_exact_preservation(self):
        task=mod.load_tasks()[0]
        source=' '.join(task['anchors']+task['qualifiers'])
        value={'evidence_copy':task['anchors'],'qualifier_copy':task['qualifiers'],'summary_ptbr':source,'caveat_ptbr':' '.join(task['qualifiers']) or 'Sem qualifier adicional.'}
        q=mod.validate_output(task,value)
        self.assertTrue(q['exact_anchor_copy'])
        self.assertTrue(q['exact_qualifier_copy'])
        self.assertEqual(q['numeric_recall'],1.0)
        self.assertTrue(q['no_unsupported_numeric_facts'])
        self.assertTrue(q['preservation_pass'])

    def test_quality_checker_rejects_unsupported_number(self):
        task=mod.load_tasks()[0]
        value={'evidence_copy':task['anchors'],'qualifier_copy':task['qualifiers'],'summary_ptbr':'Número inventado 999999999.','caveat_ptbr':'Cuidado.'}
        q=mod.validate_output(task,value)
        self.assertFalse(q['no_unsupported_numeric_facts'])
        self.assertFalse(q['preservation_pass'])

    def test_models_and_pricing_snapshot_are_fixed(self):
        self.assertEqual(mod.MODELS,('openai/gpt-oss-120b','openai/gpt-oss-20b'))
        import json
        pricing=json.loads(mod.PRICING.read_text())
        for m in mod.MODELS:
            self.assertIn(m,pricing['models'])
            self.assertIn('source_url',pricing['models'][m])


if __name__=='__main__': unittest.main()
