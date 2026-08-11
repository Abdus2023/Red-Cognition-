#!/usr/bin/env python3
"""Deep audit suite #5 (KB message #19, directive 'Deeply Verification').
Run from the repository root: python3 knowledge-base/reports/message-019-verification-suite.py
Corpus scope: messages 1..18 processed, sub-messages [1]..[180], SN-001..SN-1093,
12 specs + 46 rfcs scaffolded files."""
import re, glob, os, sys

KB = 'knowledge-base'
results = []
def check(cat, name, ok, detail=''):
    results.append((cat, name, bool(ok), detail))
    print(('PASS' if ok else 'FAIL'), '[%s]' % cat, name, ('| ' + detail if detail else ''))

fence_re = re.compile(r'^[^\S\n]*```[^\n]*\n(.*?)^[^\S\n]*```[^\n]*$', re.M | re.S)

MSG_PARTS = {2: 2, 3: 4, 5: 5, 8: 5, 10: 5, 12: 5, 14: 5, 16: 5, 18: 5}
EXPECTED_RANGES = {2: (1, 20), 3: (21, 40), 5: (41, 60), 8: (61, 80), 10: (81, 100),
                   12: (101, 120), 14: (121, 140), 16: (141, 160), 18: (161, 180)}
SN_RANGES = {2: (1, 123), 3: (124, 212), 5: (213, 318), 8: (319, 427), 10: (428, 493),
             12: (494, 640), 14: (641, 825), 16: (826, 993), 18: (994, 1093)}

def archive_files(msg):
    if msg == 1:
        return [f'{KB}/sources/message-001-original.md']
    n = MSG_PARTS[msg]
    if n == 1:
        return [f'{KB}/sources/message-{msg:03d}-original.md']
    return [f'{KB}/sources/message-{msg:03d}-original-part{k}.md' for k in range(1, n + 1)]

archive_text = {}   # msg -> concatenated text
archive_blocks = {} # msg -> list of fenced blocks
all_blocks = []
for msg in [1, 2, 3, 5, 8, 10, 12, 14, 16, 18]:
    fs = archive_files(msg)
    txt = '\n'.join(open(f, encoding='utf-8').read() for f in fs if os.path.exists(f))
    archive_text[msg] = txt
    bl = fence_re.findall(txt)
    archive_blocks[msg] = bl
    all_blocks.extend(bl)

wiki_pages = sorted(glob.glob(f'{KB}/wiki/*.md'))
wiki_all = '\n'.join(open(p, encoding='utf-8').read() for p in wiki_pages)
cs = open(f'{KB}/wiki/Code-Snippets.md', encoding='utf-8').read()

# ---------- Category 1: Archive structure ----------
missing_files = [f for m in [1,2,3,5,8,10,12,14,16,18] for f in archive_files(m) if not os.path.exists(f)]
check(1, 'all archive files exist (43 files)', not missing_files, str(missing_files))
labels, speaker_ok = [], True
for m in [2,3,5,8,10,12,14,16,18]:
    for mm in re.finditer(r'^## \[(\d+)\] ?(.*)$', archive_text[m], re.M):
        labels.append(int(mm.group(1)))
        if not mm.group(2).strip():
            speaker_ok = False
check(1, 'sub-message labels [1]..[180] contiguous (180/180)', labels == list(range(1, 181)),
      'count=%d' % len(labels))
check(1, 'every sub-message header carries a speaker label', speaker_ok)

# ---------- Category 2: Snippet annex integrity ----------
tok_ok, miss = True, []
for i in range(1, 1094):
    tok = 'SN-%03d' % i if i < 1000 else 'SN-%d' % i
    if not re.search(r'(?<![0-9A-Z-])' + tok + r'(?!\d)', cs):
        tok_ok = False; miss.append(tok)
check(2, 'SN-001..SN-1093 all present in Code-Snippets', tok_ok, str(miss[:5]))
tot = re.search(r'\*\*Corpus totals: (\d+) snippets\*\*', cs)
check(2, 'Code-Snippets corpus totals line = 1093', tot and tot.group(1) == '1093',
      tot.group(1) if tot else 'missing')
ledger_rows = re.findall(r'^\| (SN-\d{3}) \|', cs, re.M)
check(2, 'message #2 ledger has 123 rows', len(ledger_rows) == 123, str(len(ledger_rows)))
for m in (16, 18):
    bt = re.search(r'Message #%d breakdown:(.*?)(?=Message #\d+ breakdown:|## |\Z)' % m, cs, re.S)
    rows = re.findall(r'\| \[(\d+)\] \| (\d+) \|', bt.group(1)) if bt else []
    lo, hi = EXPECTED_RANGES[m]
    exp_total = SN_RANGES[m][1] - SN_RANGES[m][0] + 1
    okrows = (len(rows) == hi - lo + 1 and sum(int(r[1]) for r in rows) == exp_total
              and all(lo <= int(r[0]) <= hi for r in rows))
    check(2, 'message #%d breakdown table: %d rows sum=%d' % (m, hi-lo+1, exp_total), okrows,
          'rows=%d sum=%d' % (len(rows), sum(int(r[1]) for r in rows)))
fence_total = len(all_blocks)
check(2, 'archive fenced total = 1090 (1093 - 3 inline msg#2)', fence_total == 1090, str(fence_total))
check(2, 'message #18 archive fenced = 100', len(archive_blocks[18]) == 100, str(len(archive_blocks[18])))

# annex ordering per message
seq_ok, seq_detail = True, []
for m in (16, 18):
    lo, hi = SN_RANGES[m]
    hdr = re.search(r'## Message #%d Annex' % m, cs)
    seg = cs[hdr.start():]
    nums = [int(x) for x in re.findall(r'\*\*SN-(\d+)\*\*', seg)]
    nums = [n for n in nums if lo <= n <= hi]
    if nums != list(range(lo, hi + 1)):
        seq_ok = False; seq_detail.append('msg%d:%d' % (m, len(nums)))
check(2, 'annex SN sequences ascending & complete (msg#16, msg#18)', seq_ok, str(seq_detail))

# ---------- Category 3: Scaffolded documents ----------
specs = sorted(f for f in os.listdir('specs') if f.endswith('.md'))
rfcs = sorted(f for f in os.listdir('rfcs') if f.endswith('.md'))
check(3, 'specs/ = 12 documents', len(specs) == 12, str(len(specs)))
check(3, 'rfcs/ = 46 files', len(rfcs) == 46, str(len(rfcs)))
rfc_docs = [f for f in rfcs if 'ratification' not in f]
records = [f for f in rfcs if 'ratification' in f]
ids = sorted(int(re.match(r'RFC-(\d{4})', f).group(1)) for f in rfc_docs)
check(3, 'RFC-0001..0042 exactly once each', ids == list(range(1, 43)), '%d docs' % len(rfc_docs))
rec_ids = sorted(int(re.match(r'RFC-(\d{4})', f).group(1)) for f in records)
check(3, 'ratification records = 0001, 0002, 0011, 0042', rec_ids == [1, 2, 11, 42], str(rec_ids))

full_archive = '\n'.join(archive_text[m] for m in [1,2,3,5,8,10,12,14,16,18])
def norm(s): return '\n'.join(l.rstrip() for l in s.split('\n')).strip()
norm_full = norm(full_archive)
prov_ok, faithful, unfaithful = True, 0, []
for path in [ 'specs/' + f for f in specs ] + [ 'rfcs/' + f for f in rfcs ]:
    t = open(path, encoding='utf-8').read()
    if 'KB-Scaffold Provenance' not in t[:600]:
        prov_ok = False; print('   no provenance header:', path)
    i = t.find('-->')
    body = (t[i+3:] if i >= 0 else t).strip()
    j = body.find('<!-- KB note:')
    if j >= 0: body = body[:j].strip()
    if body in full_archive or norm(body) in norm_full:
        faithful += 1
    else:
        unfaithful.append(path)
check(3, 'all 58 scaffolds carry KB provenance headers', prov_ok)
check(3, 'all 58 scaffold bodies verbatim from archive', faithful == 58,
      'faithful=%d missing=%s' % (faithful, unfaithful))

# ---------- Category 4: Wiki fidelity & provenance ----------
exact = normed = missing = 0
missing_samples = []
normed_samples = []
norm_wiki = norm(wiki_all)
for b in all_blocks:
    if b in wiki_all: exact += 1
    elif norm(b) in norm_wiki:
        normed += 1
        if len(normed_samples) < 3: normed_samples.append(b[:70].replace('\n', '\\n'))
    else:
        missing += 1
        if len(missing_samples) < 3: missing_samples.append(b[:60].replace('\n', '\\n'))
check(4, '1090/1090 archived fenced blocks verbatim in Wiki', missing == 0,
      'exact=%d normed=%d missing=%d %s normed=%s' % (exact, normed, missing, missing_samples, normed_samples))
prov_pages = [p for p in wiki_pages if re.search(r'^>? ?\*?\*?Provenance|^> Provenance', open(p, encoding='utf-8').read()[:1200], re.M)]
check(4, 'wiki pages with provenance headers (>= 17 core content pages)', len(prov_pages) >= 17,
      '%d: %s' % (len(prov_pages), [os.path.basename(p) for p in prov_pages]))
reps = sorted(glob.glob(f'{KB}/reports/message-*-report.md'))
need = ['message-%03d-report.md' % i for i in range(1, 20)]
have = set(os.path.basename(r) for r in reps)
check(4, 'reports message-001..019 exist', all(n in have for n in need), str(len(reps)))
link_re = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')
broken = []
for md in glob.glob(f'{KB}/*.md') + wiki_pages + glob.glob(f'{KB}/reports/*.md'):
    base = os.path.dirname(md)
    for _, target in link_re.findall(open(md, encoding='utf-8').read()):
        if re.match(r'^(https?:|mailto:|#)', target): continue
        t = target.split('#')[0]
        if t and not os.path.exists(os.path.normpath(os.path.join(base, t))):
            broken.append((os.path.basename(md), target))
check(4, 'internal markdown links all resolve (0 broken)', not broken, str(broken[:5]))
check(4, 'KB directories sources/ wiki/ reports/ exist',
      all(os.path.isdir(f'{KB}/{d}') for d in ('sources', 'wiki', 'reports')))

# ---------- Category 5: Normative consistency (message #18 material) ----------
chain = {34: 'RFC-0033', 35: 'RFC-0034', 36: 'RFC-0035', 37: 'RFC-0036', 38: 'RFC-0037',
         39: 'RFC-0038', 40: 'RFC-0039', 41: 'RFC-0040', 42: 'RFC-0041'}
chain_ok, chain_bad = True, []
for n, parent in chain.items():
    f = [x for x in rfc_docs if x.startswith('RFC-%04d-' % n)][0]
    t = open('rfcs/' + f, encoding='utf-8').read()
    m = re.search(r'\*\*Parent:\*\* (RFC-\d{4})', t)
    if not (m and m.group(1) == parent):
        chain_ok = False; chain_bad.append('%04d->%s' % (n, m.group(1) if m else None))
check(5, 'RFC-0034..0042 Parent headers form the documented chain', chain_ok, str(chain_bad))
rec42 = open('rfcs/RFC-0042-ratification-record.md', encoding='utf-8').read()
check(5, 'ratification record: "Ratified as the operational orchestration layer"',
      'Ratified as the operational orchestration layer' in rec42)
tab_ids = sorted(int(x) for x in re.findall(r'^\| RFC-(\d{4})', rec42, re.M))
check(5, 'ratification record status table covers RFC-0001..0041 (41 rows; 0042 is the ratified subject)',
      tab_ids == list(range(1, 42)), 'rows=%d' % len(tab_ids))
r34 = open('rfcs/RFC-0034-cpr-tdp-package-registry.md', encoding='utf-8').read()
check(5, 'RFC-0034 defines trust levels T0..T5', all(('T%d' % k) in r34 for k in range(0, 6)))
r42 = open('rfcs/RFC-0042-cadp-autonomous-deployment.md', encoding='utf-8').read()
lifecycle = 'design → compile → verify → package → distribute → govern → federate → deploy → monitor → evolve → retire'
check(5, 'CADP lifecycle chain present (RFC-0042 or record/index)',
      lifecycle in r42 or lifecycle in rec42 or lifecycle in wiki_all)
check(5, '[175] <|eos|> truncation artifact preserved in archive', '<|eos|>' in archive_text[18])
dup_count = archive_text[18].count('Cognitive Package Registry and Trust Distribution Protocol (CPR-TDP)')
check(5, 'duplicated RFC-0034 text preserved in [167] (title occurs >= 3x in msg#18 archive)',
      dup_count >= 3, str(dup_count))
future = [f for f in rfcs if int(re.match(r'RFC-(\d{4})', f).group(1)) > 42]
ri = open(f'{KB}/wiki/RFC-Index.md', encoding='utf-8').read()
check(5, 'RFC-0043..0050 proposals NOT scaffolded, recorded in RFC-Index', not future and 'RFC-0043' in ri)
groups = ['Semantic Foundation', 'Execution & Recovery', 'Runtime & Infrastructure',
          'Operating System & Governance', 'Hardware & Compiler', 'Distribution & Ecosystem',
          'Operational Lifecycle']
check(5, 'stack grouping (7 cohorts) recorded in RFC-Index', all(g in ri for g in groups))
gl = open(f'{KB}/wiki/Glossary.md', encoding='utf-8').read()
terms = ['CPR-TDP', 'CSEIM', 'CBR-SCP', 'CSLEMP', 'CMAEP', 'CIEOP', 'CGCDP', 'CIFP', 'CADP']
check(5, 'Glossary contains ecosystem-plane acronyms (9/9)', all(t in gl for t in terms),
      str([t for t in terms if t not in gl]))
st = open(f'{KB}/wiki/Source-Traceability.md', encoding='utf-8').read()
check(5, 'conflicts C-9 & C-10 recorded with resolution notes',
      '| C-9 |' in st and '| C-10 |' in st and 'authoritative' in st)
check(5, 'duplicates D-58..D-62 recorded', all(('| D-%d |' % d) in st for d in range(58, 63)))

# ---------- Category 6: RFC parent-chain integrity ----------
no_parent = []
for f in rfc_docs:
    t = open('rfcs/' + f, encoding='utf-8').read()
    if '**Parent:**' not in t and 'Parent:' not in t[:1200]:
        no_parent.append(f)
check(6, 'all 42 RFC documents carry a Parent header', not no_parent, str(no_parent))
chain24_ok, bad24 = True, []
for n in range(24, 43):
    f = [x for x in rfc_docs if x.startswith('RFC-%04d-' % n)][0]
    t = open('rfcs/' + f, encoding='utf-8').read()
    m = re.search(r'\*\*Parent:\*\* (RFC-\d{4})', t)
    if not (m and m.group(1) == 'RFC-%04d' % (n - 1)):
        chain24_ok = False; bad24.append(n)
check(6, 'contiguous parent chain RFC-0024..0042 (each parent = preceding RFC)', chain24_ok, str(bad24))

# ---------- Category 7: Status & cross-page coherence ----------
readme = open(f'{KB}/README.md', encoding='utf-8').read()
check(7, 'README totals (messages/snippets/specs/rfcs)',
      all(s in readme for s in ['19 messages processed', '**1093 code snippets**',
                                '**12 scaffolded documents in `specs/`**', '**46 files in `rfcs/`**']))
idx_rows = re.findall(r'^\| RFC-(00[34]\d) \|[^\n]*$', ri, re.M)
draft_ok = True
for n in range(34, 42):
    row = [r for r in re.findall(r'^\| RFC-%04d \|.*$' % n, ri, re.M)]
    if not row or 'Draft' not in row[0]:
        draft_ok = False; print('   row status issue RFC-%04d' % n)
check(7, 'RFC-Index rows RFC-0034..0041 = Draft', draft_ok)
row42 = re.findall(r'^\| RFC-0042 \|.*$', ri, re.M)
check(7, 'RFC-Index row RFC-0042 = Ratified', bool(row42) and re.search(r'RATIFIED|Ratified', row42[0]))
ratset_ok = all(s in ri for s in ['RC-000', 'RC-100', 'RC-200', 'RFC-0001', 'RFC-0002', 'RFC-0011', 'RFC-0042'])
check(7, 'ratified set enumerated in RFC-Index', ratset_ok)
cl = open(f'{KB}/wiki/Changelog.md', encoding='utf-8').read()
miss_cl = [i for i in range(1, 19) if ('Message #%d' % i) not in cl]
check(7, 'changelog entries for messages 1..18 + finalization', not miss_cl and 'finalization' in cl, str(miss_cl))

# ---------- Category 8: Traceability bookkeeping ----------
reg = sorted(set(int(m) for m in re.findall(r'^\| (\d+) \| 2026-', st, re.M)))
check(8, 'register rows 1..19 contiguous', reg == list(range(1, 20)), str(reg))
idx_count = len(re.findall(r'^#{2,3} Message #\d+ sub-message index', st, re.M))
check(8, 'sub-message indexes for msgs 2,3,5,8,10,12,14,16,18 (9 indexes)', idx_count == 9, str(idx_count))
xs = sorted(set(int(m) for m in re.findall(r'^\| X-(\d+) \|', st, re.M)))
check(8, 'cross-references contiguous X-01..X-87', xs == list(range(1, 88)), 'count=%d' % len(xs))
ds = sorted(set(int(m) for m in re.findall(r'^\| D-(\d+) \|', st, re.M)))
check(8, 'duplicate log contiguous D-1..D-62', ds == list(range(1, 63)), 'count=%d' % len(ds))
csids = sorted(set(int(m) for m in re.findall(r'^\| C-(\d+) \|', st, re.M)))
check(8, 'conflict log contiguous C-1..C-10', csids == list(range(1, 11)), str(csids))
mandated = ['specs', 'rfcs', 'compiler', 'runtime', 'dialects', 'cognition', 'tests', 'examples', 'docs']
check(8, 'RC-000 section 8 mandated directories exist (9/9)', all(os.path.isdir(d) for d in mandated),
      str([d for d in mandated if not os.path.isdir(d)]))

fails = [r for r in results if not r[2]]
bycat = {}
for c, n, ok, d in results:
    bycat.setdefault(c, [0, 0])
    bycat[c][1] += 1
    if ok: bycat[c][0] += 1
print('\nPer-category:', {c: '%d/%d' % tuple(v) for c, v in sorted(bycat.items())})
print('%d/%d checks passed' % (len(results) - len(fails), len(results)))
sys.exit(1 if fails else 0)
