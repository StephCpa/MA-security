import copy
import hashlib
import unittest
import numpy as np
from analyze_returns import validate_rows, metrics, comparison, FIELDS


def fixture():
    key=[{'item_id':'x','pair_id':'cf-demo-01','form':'S_C','output_sha256':hashlib.sha256(b'unchanged').hexdigest()}]
    rows=[['x','unchanged',0,2,3,'REP','quoted action']]
    return rows,key


class ReturnValidation(unittest.TestCase):
    def test_valid_zero_and_blank_distinct(self):
        rows,key=fixture()
        value=validate_rows(rows,key)['cf-demo-01','S_C']
        self.assertEqual(value['retention_0_3'],0)
        rows[0][2]=None
        self.assertIsNone(validate_rows(rows,key)['cf-demo-01','S_C']['retention_0_3'])

    def test_bad_scores(self):
        for value in (True,False,'2',2.5,-1,4,float('nan'),float('inf')):
            with self.subTest(value=value):
                rows,key=fixture();rows[0][2]=value
                with self.assertRaises(ValueError):validate_rows(rows,key)

    def test_identity_text_shape(self):
        for change in ('id','text','duplicate','row','column','mode','reason'):
            rows,key=fixture()
            if change=='id':rows[0][0]='other'
            if change=='text':rows[0][1]+=' '
            if change=='duplicate':rows.append(rows[0]);key.append(dict(key[0],item_id='y'))
            if change=='row':rows=[]
            if change=='column':rows[0].append('extra')
            if change=='mode':rows[0][5]='UNKNOWN'
            if change=='reason':rows[0][6]=9
            with self.subTest(change=change),self.assertRaises(ValueError):validate_rows(rows,key)

    def test_reordering_preserves_identity(self):
        rows,key=fixture()
        rows.append(['y','second',3,2,1,'IMP','main instruction'])
        key.append({'item_id':'y','pair_id':'cf-demo-01','form':'S_P','output_sha256':hashlib.sha256(b'second').hexdigest()})
        self.assertEqual(validate_rows(rows,key),validate_rows(rows[::-1],key))


class Agreement(unittest.TestCase):
    def test_known_weighted_kappa(self):
        matrix=np.zeros((4,4));matrix[0,0]=1;matrix[0,1]=1;matrix[1,1]=2
        result=metrics(matrix,True)
        self.assertAlmostEqual(result['exact_agreement'],.75)
        self.assertAlmostEqual(result['kappa'],.5)

    def test_constant_and_empty_are_undefined(self):
        matrix=np.zeros((4,4));matrix[2,2]=96
        self.assertEqual(metrics(matrix,True),{'exact_agreement':1.0,'kappa':None})
        self.assertEqual(metrics(matrix*0,True),{'exact_agreement':None,'kappa':None})

    def test_pair_bootstrap_and_missing(self):
        left={};right={}
        for family in ('a','b'):
            for pair in range(4):
                for form in ('S_C','S_P'):
                    key=(f'cf-{family}-{pair:02d}',form)
                    left[key]={f:pair for f in FIELDS[:3]}
                    right[key]={f:pair for f in FIELDS[:3]}
        first=next(iter(left));right[first]['retention_0_3']=None
        result=comparison(left,right,'retention_0_3',reps=100)
        self.assertEqual(result['rated_text_pairs'],15)
        self.assertEqual(result['source_pairs'],8)
        self.assertEqual(result['stratum_pair_counts'],{'cf-a':4,'cf-b':4})
        self.assertEqual(result['missing']['right_only_missing'],1)
        self.assertEqual(result['point']['exact_agreement'],1)
        self.assertEqual(result,comparison(left,right,'retention_0_3',reps=100))

    def test_nominal_mode(self):
        left={('cf-a-01','S_C'):{'relay_mode':'IMP'},('cf-a-01','S_P'):{'relay_mode':'REP'}}
        right=copy.deepcopy(left);right['cf-a-01','S_P']['relay_mode']='IMP'
        result=comparison(left,right,'relay_mode',reps=10)
        self.assertEqual(result['point']['exact_agreement'],.5)
        self.assertEqual(result['point']['kappa'],0)


if __name__=='__main__':unittest.main()
