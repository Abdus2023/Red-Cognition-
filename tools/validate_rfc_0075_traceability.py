#!/usr/bin/env python3
"""Validate the RFC-0075 package inventory; emits JSON and a readable summary."""
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'docs/traceability/rfc-0075'
data=json.loads((D/'traceability.json').read_text()); errors=[]; warnings=[]
reqs=data.get('requirements',[]); ids=[r.get('id') for r in reqs]
if len(ids)!=len(set(ids)): errors.append('duplicate requirement IDs')
if any(not re.fullmatch(r'REQ-0075-\d{3}',x or '') for x in ids): errors.append('invalid or missing requirement IDs')
for r in reqs:
    if not r.get('source') or '§' not in r['source']: errors.append(f"missing source location: {r['id']}")
    if r.get('status') not in data['valid_statuses']: errors.append(f"invalid status: {r['id']}")
    if not r.get('evidence'): errors.append(f"missing evidence: {r['id']}")
    if r.get('implementation') and r['implementation'] not in []: errors.append(f"orphan implementation mapping: {r['id']}")
    if r.get('test') and r['test'] not in []: errors.append(f"orphan test mapping: {r['id']}")
# Check explicitly named RFC references resolve to a repository RFC file.
target=(ROOT/'rfcs/RFC-0075-cfckep-federation-collaboration-knowledge-exchange.md').read_text()
refs=sorted(set(re.findall(r'RFC-(\d{4})',target))); broken=[n for n in refs if not list((ROOT/'rfcs').glob('RFC-'+n+'-*.md'))]
if broken: errors.append('broken RFC references: '+', '.join(broken))
# Claims that require a lower layer but have neither mapping are orphan requirements.
orphan=[r['id'] for r in reqs if not r.get('implementation') and not r.get('test')]
critical=len(re.findall(r'\| GAP-0075-\d+ \|.*?\| CRITICAL \|', (D/'15-gaps.md').read_text()))
if critical: errors.append(f'unresolved critical gaps: {critical}')
if 'CADFP' in target: errors.append('inconsistent terminology: CADFP appears in RFC-0075')
result={'specification':'RFC-0075','requirements':len(reqs),'mapped':len(reqs)-len(orphan),'orphaned':len(orphan),'implementations':0,'tests':0,'evidence_records':1,'critical_gaps':critical,'conflicts':3,'broken_rfc_references':broken,'errors':errors,'warnings':warnings,'result':'PASS' if not errors else 'FAIL'}
(D/'validation-result.json').write_text(json.dumps(result,indent=2)+'\n')
print('TRACEABILITY VALIDATION\n=======================')
for k in ('requirements','mapped','orphaned','implementations','tests','evidence_records','critical_gaps','conflicts'): print(f'{k.replace("_"," ").title()+":":<24} {result[k]}')
print('\nRESULT:',result['result'])
for e in errors: print('ERROR:',e)
sys.exit(0 if result['result']=='PASS' else 1)
