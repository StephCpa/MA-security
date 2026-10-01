import json
import unittest
from audit_selector_transportability import classify, cp
from test_selector_transportability import response


def event(record):
    return {'kind': 'response', 'data': {'http_status': record['HttpStatus'], 'body_text': json.dumps(record['Response'])}}


class SelectorAuditTests(unittest.TestCase):
    def test_exact_limits(self):
        self.assertAlmostEqual(cp(0, 16, .95)[1], 1 - .025 ** (1/16))
        self.assertEqual(cp(0, 16, .95)[0], 0)
        self.assertAlmostEqual(cp(16, 16, .95)[0], .025 ** (1/16))

    def test_independent_classifier(self):
        self.assertEqual(classify(event(response())), (True, 'unchanged'))
        self.assertEqual(classify(event(response('summarize', {'summary': 'safe'}))), (False, None))
        self.assertEqual(classify(event(response(finish='length'))), (None, None))
        record = response()
        record['Response']['choices'][0]['message']['tool_calls'][0]['function']['arguments'] = '{"target":"x","target":"y","payload":"z"}'
        self.assertEqual(classify(event(record)), (None, None))


if __name__ == '__main__':
    unittest.main()
