#!/usr/bin/env python3
"""Strict, dependency-free validator for the RFC-0075 traceability inventory.
Writes docs/traceability/rfc-0075/validation-result.json and exits non-zero on FAIL.
"""
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'docs/traceability/rfc-0075'
required_docs=['README.md','00-overview.md','01-source-authority.md','02-requirements.md','03-traceability-matrix.md','04-architecture-traceability.md','05-rfc-dependencies.md','06-invariants.md','07-data-models.md','08-lifecycle.md','09-security-traceability.md','10-determinism-replay.md','11-observability.md','12-implementation-mapping.md','13-test-mapping.md','14-evidence.md','15-gaps.md','16-conflicts.md','17-terminology.md','18-conformance.md','manifest.yaml','traceability.json']
errors=[]; warnings=[]
for name in required_docs:
    if not (D/name).is_file(): errors.append(f'missing package artifact: {name}')
data=json.loads((D/'traceability.json').read_text()); target=ROOT/'rfcs/RFC-0075-cfckep-federation-collaboration-knowledge-exchange.md'
if not target.is_file(): errors.append('missing authoritative RFC-0075 source')
text=target.read_text() if target.is_file() else ''
def unique(records, key, label, pattern=None):
    values=[x.get(key) if isinstance(x,dict) else x for x in records]
    if any(not v for v in values): errors.append(f'missing {label} IDs')
    if len(values)!=len(set(values)): errors.append(f'duplicate {label} IDs')
    if pattern and any(not re.fullmatch(pattern,str(v)) for v in values if v): errors.append(f'invalid {label} IDs')
reqs=data.get('requirements',[]); unique(reqs,'id','requirement',r'REQ-0075-\d{3}')
unique(data.get('architectural_concepts',[]),'id','architecture concept',r'ARCH-0075-\d{3}')
unique(data.get('models',[]),'id','model field',r'MODEL-0075-\d{3}-[A-Za-z][A-Za-z0-9]*')
unique(data.get('evidence_records',[]),'id','evidence',r'EVID-0075-\d{3}')
unique(data.get('gaps',[]),'id','gap',r'GAP-0075-\d{3}')
unique(data.get('conflicts',[]),None,'conflict',r'CONFLICT-0075-\d{3}')
evidence={x['id'] for x in data.get('evidence_records',[])}; statuses=set(data.get('valid_statuses',[]))
for r in reqs:
    rid=r.get('id','<unknown>'); source=r.get('source','')
    if not source or '§' not in source: errors.append(f'missing source location: {rid}')
    elif source.startswith('rfcs/RFC-0075'):
        sec=source.rsplit('§',1)[1]
        if not re.search(r'^###\s+'+re.escape(sec)+r'[. ]',text,re.M): errors.append(f'broken source section: {rid} → {sec}')
    if r.get('status') not in statuses: errors.append(f'invalid status: {rid}')
    if not r.get('evidence'): errors.append(f'missing evidence: {rid}')
    for eid in r.get('evidence',[]):
        if eid not in evidence: errors.append(f'broken evidence reference: {rid} → {eid}')
impl_ids={x.get('id') for x in data.get('implementations',[])}; test_ids={x.get('id') for x in data.get('tests',[])}
for r in reqs:
    if r.get('implementation') and r['implementation'] not in impl_ids: errors.append(f'orphan implementation mapping: {r["id"]}')
    if r.get('test') and r['test'] not in test_ids: errors.append(f'orphan test mapping: {r["id"]}')
refs=sorted(set(re.findall(r'RFC-(\d{4})',text))); broken=[n for n in refs if not list((ROOT/'rfcs').glob(f'RFC-{n}-*.md'))]
if broken: errors.append('broken RFC references: '+', '.join(broken))
# An unimplemented/untested requirement is an explicit traceability orphan, not a validator defect.
orphan=[r['id'] for r in reqs if not r.get('implementation') and not r.get('test')]
critical=sum(x.get('severity')=='CRITICAL' for x in data.get('gaps',[]))
if critical: errors.append(f'unresolved critical gaps: {critical}')
if 'CADFP' in text: errors.append('inconsistent terminology: CADFP appears in RFC-0075')
result={'specification':'RFC-0075','requirements':len(reqs),'mapped':len(reqs)-len(orphan),'orphaned':len(orphan),'implementations':len(impl_ids),'tests':len(test_ids),'evidence_records':len(evidence),'critical_gaps':critical,'conflicts':len(data.get('conflicts',[])),'broken_rfc_references':broken,'errors':errors,'warnings':warnings,'result':'PASS' if not errors else 'FAIL'}
(D/'validation-result.json').write_text(json.dumps(result,indent=2)+'\n')
print('TRACEABILITY VALIDATION\n=======================')
for k in ('requirements','mapped','orphaned','implementations','tests','evidence_records','critical_gaps','conflicts'): print(f'{k.replace("_"," ").title()+":":<24} {result[k]}')
print('\nRESULT:',result['result'])
for e in errors: print('ERROR:',e)
sys.exit(0 if result['result']=='PASS' else 1)
