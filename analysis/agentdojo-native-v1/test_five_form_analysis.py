import unittest
from analyze_five_form import contrast

class Tests(unittest.TestCase):
    def test_complete(self):
        r=contrast([True,True,False,False],[True,False,True,False])
        self.assertEqual(r['risk_difference'],0)
        self.assertEqual(r['paired_table'],dict(both_success=1,a_only=1,b_only=1,both_failure=1,unknown_pair=0))
    def test_missing(self):
        self.assertEqual(contrast([None],[None])['missingness_bounds'],[-1,1])
        self.assertEqual(contrast([True],[None])['missingness_bounds'],[0,1])
        self.assertEqual(contrast([None],[True])['missingness_bounds'],[-1,0])
    def test_mixed(self):
        r=contrast([True,None],[False,True]);self.assertEqual(r['missingness_bounds'],[0,.5]);self.assertIsNone(r['risk_difference'])

if __name__=='__main__':unittest.main()
