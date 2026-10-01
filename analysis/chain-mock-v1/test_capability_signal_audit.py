import unittest
from audit_capability_signal import paired


class PairingTests(unittest.TestCase):
    def test_zero_discordance_has_nonzero_interval(self):
        r=paired([(True,True)]*45+[(False,False)]*3,primary=True)
        self.assertEqual(r['risk_difference_signal_minus_silent'],0)
        self.assertEqual(r['two_sided_exact_McNemar_p'],1)
        bound=1-.0125**(1/48)
        self.assertAlmostEqual(r['conservative_95_paired_projection'][1],bound)

    def test_missing_and_secondary(self):
        r=paired([(None,False),(True,None)],primary=True)
        self.assertEqual(r['rd_missingness_bounds'],[-1,0])
        self.assertNotIn('two_sided_exact_McNemar_p',r)
        secondary=paired([(False,True)]*7+[(True,False)]+[(True,True)]*28+[(False,False)]*12)
        self.assertEqual(secondary['risk_difference_signal_minus_silent'],.125)
        self.assertNotIn('two_sided_exact_McNemar_p',secondary)


if __name__=='__main__':unittest.main()
