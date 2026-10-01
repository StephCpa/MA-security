"""Descriptive raw-text supplement; lexical flags are not semantic ratings."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path


def describe(path):
    path = Path(path)
    plan = json.loads((path / 'manifest.json').read_text(encoding='utf-8'))
    events = [json.loads(x) for x in (path / 'events.jsonl').read_text(encoding='utf-8').splitlines()]
    outcomes = [json.loads(x) for x in (path / 'outcomes.jsonl').read_text(encoding='utf-8').splitlines()]
    cases = {c['directive_id']: c for c in plan['cases']}
    senders, incomplete, attack_writes = [], [], []
    for event in events:
        if event['kind'] != 'response':
            continue
        body = json.loads(event['data']['body_text'])
        if not body.get('choices'):
            continue
        choice = body['choices'][0]
        if choice['finish_reason'] not in ('stop', 'tool_calls'):
            incomplete.append({'call_id': event['call_id'], 'finish_reason': choice['finish_reason']})
        item, arm, stage, _ = event['call_id'].split('::')
        if stage == 'sender' and cases[item]['kind'] == 'benign':
            text = choice['message'].get('content') or ''
            senders.append({'directive_id': item, 'wording': cases[item].get('wording', 'original'),
                            'form': arm, 'text': text,
                            'contains_retrieve': bool(re.search(r'\bretrieve\b', text, re.I)),
                            'contains_write': bool(re.search(r'\bwrite\b', text, re.I))})
    groups = {}
    for row in outcomes:
        case = cases[row['directive_id']]
        key = '/'.join((case['kind'], case.get('wording', 'not_applicable'), row['arm']))
        group = groups.setdefault(key, Counter())
        group['n'] += 1
        if case['kind'] == 'benign':
            value = row['legitimate_exact_write']
            group['exact_' + ('unknown' if value is None else str(value).lower())] += 1
        for endpoint in ('any_write_request', 'protected_request'):
            value = row['request_endpoints'][endpoint]
            group[endpoint + '_' + ('unknown' if value is None else str(value).lower())] += 1
        if case['kind'] == 'attack':
            for branch in row['branches']:
                for decision in branch['gateway_decisions']:
                    attack_writes.append({'directive_id': row['directive_id'], 'arm': row['arm'], **decision})
    return {'scope': 'Descriptive diagnostic; no tests, confidence intervals or semantic-judge labels.',
            'groups': groups, 'benign_sender_texts': senders,
            'incomplete_responses': incomplete, 'attack_gateway_decisions': attack_writes}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run_dir')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = describe(args.run_dir)
    with Path(args.output).open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'groups': result['groups'], 'incomplete': result['incomplete_responses']}, indent=2))
