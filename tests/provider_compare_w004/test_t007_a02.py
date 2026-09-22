from __future__ import annotations
import unittest
from experiments.provider_compare_w004 import run_t007_a02 as mod


class T007A02Tests(unittest.TestCase):
    def test_population_and_models_are_fixed(self):
        tasks=mod.load_tasks()
        self.assertEqual(len(tasks),4)
        self.assertEqual(mod.MODELS,('openai/gpt-oss-120b','openai/gpt-oss-20b'))
        self.assertTrue(all(t['concept_groups'] for t in tasks))

    def test_response_shape_is_short_and_auditable(self):
        p=mod.prompt(mod.load_tasks()[0])
        self.assertIn('summary_ptbr',p)
        self.assertIn('qualifier_copy',p)
        self.assertIn('caveat_ptbr',p)
        self.assertNotIn('evidence_copy MUST',p)
        self.assertEqual(mod.MAX_OUTPUT_TOKENS,1536)

    def test_quality_checker_accepts_preserved_source(self):
        task=mod.load_tasks()[0]
        # The response contract is PT-BR. Preserve the source text/numerics and include
        # the faithful Portuguese rendering of the restrictive-stance qualifier.
        text=' '.join(task['anchors']+task['qualifiers']) + ' política monetária restritiva'
        value={'summary_ptbr':text,'qualifier_copy':task['qualifiers'],'caveat_ptbr':' '.join(task['qualifiers']) or 'Sem qualifier adicional.'}
        q=mod.validate_output(task,value)
        self.assertTrue(q['exact_qualifier_copy'])
        self.assertEqual(q['numeric_recall'],1.0)
        self.assertEqual(q['concept_recall'],1.0)
        self.assertTrue(q['no_unsupported_numeric_facts'])
        self.assertTrue(q['preservation_pass'])

    def test_quality_checker_rejects_invented_number(self):
        task=mod.load_tasks()[0]
        value={'summary_ptbr':'Selic IPCA restritiva 999999999','qualifier_copy':task['qualifiers'],'caveat_ptbr':' '.join(task['qualifiers']) or 'Cuidado.'}
        q=mod.validate_output(task,value)
        self.assertFalse(q['no_unsupported_numeric_facts'])
        self.assertFalse(q['preservation_pass'])

    def test_a03_is_not_part_of_quality_design(self):
        self.assertNotIn('model_validation_a03',mod.prompt(mod.load_tasks()[0]))


if __name__=='__main__': unittest.main()
