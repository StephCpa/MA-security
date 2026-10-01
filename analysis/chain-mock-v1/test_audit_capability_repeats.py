import unittest
from audit_capability_repeats import summarize

class RepeatAuditTests(unittest.TestCase):
    def test_flip_and_missing(self):
        data={('one',a,s,r):False for a in (0,1) for s in (0,1) for r in range(4)}
        data['one',0,0,1]=True
        data['one',1,1,2]=None
        report=summarize(data,['one'])
        self.assertEqual(report['complete_source_cells'],3)
        self.assertEqual(report['unknown_source_cells'],1)
        self.assertEqual(report['complete_cells_with_flip'],1)
        self.assertEqual(report['complete_cell_flip_fraction'],1/3)
        self.assertNotIn('two_sided_exact_McNemar_p',report['rounds']['0']['cue_contrasts']['a0'])
        self.assertEqual(report['rounds']['2']['cue_contrasts']['a1']['unknown_pairs'],1)

if __name__=='__main__':unittest.main()
