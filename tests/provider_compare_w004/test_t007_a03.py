from __future__ import annotations
import unittest
from experiments.provider_compare_w004 import run_t007_a03 as mod

class T007A03Tests(unittest.TestCase):
    def test_population_models_and_bilingual_copom_guardrail(self):
        tasks=mod.load_tasks(); self.assertEqual(len(tasks),4); self.assertEqual(mod.MODELS,('openai/gpt-oss-120b','openai/gpt-oss-20b'))
        copom=next(t for t in tasks if t['source_id']=='copom_277_2026_03')
        self.assertIn(['restritiv','restrictiv'],copom['concept_groups'])
    def test_short_response_shape(self):
        p=mod.prompt(mod.load_tasks()[0]); self.assertIn('summary_ptbr',p); self.assertIn('qualifier_copy',p); self.assertIn('caveat_ptbr',p); self.assertEqual(mod.MAX_OUTPUT_TOKENS,1536)
    def test_checker_accepts_source_text(self):
        for task in mod.load_tasks():
            text=' '.join(task['anchors']+task['qualifiers'])
            q=mod.validate_output(task,{'summary_ptbr':text,'qualifier_copy':task['qualifiers'],'caveat_ptbr':' '.join(task['qualifiers']) or 'Sem qualifier adicional.'})
            self.assertEqual(q['numeric_recall'],1.0,task['source_id']); self.assertEqual(q['concept_recall'],1.0,task['source_id']); self.assertTrue(q['preservation_pass'],task['source_id'])
    def test_checker_rejects_unsupported_number(self):
        task=mod.load_tasks()[0]; q=mod.validate_output(task,{'summary_ptbr':'Selic IPCA restrictive 999999999','qualifier_copy':task['qualifiers'],'caveat_ptbr':' '.join(task['qualifiers'])})
        self.assertFalse(q['no_unsupported_numeric_facts']); self.assertFalse(q['preservation_pass'])
    def test_no_a03_validation_gold_in_prompt(self):
        self.assertNotIn('model_validation_a03',mod.prompt(mod.load_tasks()[0]))

if __name__=='__main__': unittest.main()
