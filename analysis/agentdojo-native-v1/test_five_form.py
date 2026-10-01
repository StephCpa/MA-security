import unittest
from five_form import forms,decode,MODEL

class Tests(unittest.TestCase):
    def test_marker_only_contrast(self):
        f=forms('Read a document.')
        self.assertEqual(f['P'].replace('UNTRUSTED EMBEDDED CONTENT:\n',''),f['C'])
        self.assertTrue(f['C'].endswith(f['R']))
    def test_parse(self):
        response={'HttpStatus':200,'Response':{'model':MODEL,'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':'Summary.'}}]}}
        self.assertEqual(decode(response),('Summary.','complete'))
        response['Response']['choices'][0]['finish_reason']='length'
        self.assertIsNone(decode(response)[0])
        response['Response']['model']='different'
        self.assertEqual(decode(response)[1],'model_mismatch')
    def test_transport(self):self.assertEqual(decode({'HttpStatus':429})[1],'transport')

if __name__=='__main__':unittest.main()
