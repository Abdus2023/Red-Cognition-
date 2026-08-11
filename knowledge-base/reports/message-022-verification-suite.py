#!/usr/bin/env python3
"""Message #22 final verification suite for the Red-Cognition knowledge base.
Run from the repository root: python3 knowledge-base/reports/message-022-verification-suite.py
Corpus scope: messages 1..22 processed, sub-messages [1]..[220], SN-001..SN-1229,
12 specs + 55 rfcs scaffolded files."""
import re, glob, os, sys

KB = 'knowledge-base'
results = []
def check(cat, name, ok, detail=''):
    results.append((cat, name, bool(ok), detail))
    print(('PASS' if ok else 'FAIL'), '[%s]' % cat, name, ('| ' + detail if detail else ''))

fence_re = re.compile(r'^[^\S\n]*```[^\n]*\n(.*?)^[^\S\n]*```[^\n]*$', re.M | re.S)

TRANSCRIPT_MSGS = [2, 3, 5, 8, 10, 12, 14, 16, 18, 21, 22]
MSG_PARTS = {2: 2, 3: 4, 5: 5, 8: 5, 10: 5, 12: 5, 14: 5, 16: 5, 18: 5, 21: 5, 22: 5}
EXPECTED_RANGES = {2: (1, 20), 3: (21, 40), 5: (41, 60), 8: (61, 80), 10: (81, 100),
                   12: (101, 120), 14: (121, 140), 16: (141, 160), 18: (161, 180), 21: (181, 200), 22: (201, 220)}
SN_RANGES = {2: (1, 123), 3: (124, 212), 5: (213, 318), 8: (319, 427), 10: (428, 493),
             12: (494, 640), 14: (641, 825), 16: (826, 993), 18: (994, 1093), 21: (1094, 1138), 22: (1139, 1229)}

def archive_files(msg):
    if msg == 1:
        return [f'{KB}/sources/message-001-original.md']
    n = MSG_PARTS.get(msg, 1)
    if n == 1:
        return [f'{KB}/sources/message-{msg:03d}-original.md']
    return [f'{KB}/sources/message-{msg:03d}-original-part{k}.md' for k in range(1, n + 1)]

archive_text, archive_blocks, all_blocks = {}, {}, []
for msg in [1] + TRANSCRIPT_MSGS:
    fs = archive_files(msg)
    txt = '\n'.join(open(f, encoding='utf-8').read() for f in fs if os.path.exists(f))
    archive_text[msg] = txt
    bl = fence_re.findall(txt)
    archive_blocks[msg] = bl
    all_blocks.extend(bl)

wiki_pages = sorted(glob.glob(f'{KB}/wiki/*.md'))
wiki_all = '\n'.join(open(p, encoding='utf-8').read() for p in wiki_pages)
cs = open(f'{KB}/wiki/Code-Snippets.md', encoding='utf-8').read()

# ---------- 1. Archive structure ----------
missing = [f for m in [1] + TRANSCRIPT_MSGS for f in archive_files(m) if not os.path.exists(f)]
check(1, 'all archive files exist (53 files)', not missing, str(missing))
labels, speaker_ok = [], True
for m in TRANSCRIPT_MSGS:
    for mm in re.finditer(r'^## \[(\d+)\] ?(.*)$', archive_text[m], re.M):
        labels.append(int(mm.group(1)))
        if not mm.group(2).strip(): speaker_ok = False
check(1, 'sub-message labels [1]..[220] contiguous (220/220)', labels == list(range(1, 221)), 'count=%d' % len(labels))
check(1, 'every sub-message header carries a speaker label', speaker_ok)

# ---------- 2. Snippet annex integrity ----------
tok_ok, miss = True, []
for i in range(1, 1230):
    tok = 'SN-%03d' % i if i < 1000 else 'SN-%d' % i
    if not re.search(r'(?<![0-9A-Z-])' + tok + r'(?!\d)', cs):
        tok_ok = False; miss.append(tok)
check(2, 'SN-001..SN-1229 all present in Code-Snippets', tok_ok, str(miss[:5]))
tot = re.search(r'\*\*Corpus totals: (\d+) snippets\*\*', cs)
check(2, 'Code-Snippets corpus totals line = 1229', tot and tot.group(1) == '1229', tot.group(1) if tot else 'missing')
for m in (16, 18, 21, 22):
    bt = re.search(r'Message #%d breakdown:(.*?)(?=Message #\d+ breakdown:|Note:|## |\Z)' % m, cs, re.S)
    rows = re.findall(r'\| \[(\d+)\] \| (\d+) \|', bt.group(1)) if bt else []
    lo, hi = EXPECTED_RANGES[m]
    exp = SN_RANGES[m][1] - SN_RANGES[m][0] + 1
    ok = len(rows) == hi - lo + 1 and sum(int(r[1]) for r in rows) == exp and all(lo <= int(r[0]) <= hi for r in rows)
    check(2, 'message #%d breakdown table (%d rows, sum %d)' % (m, hi-lo+1, exp), ok,
          'rows=%d sum=%d' % (len(rows), sum(int(r[1]) for r in rows)))
check(2, 'archive fenced total = 1226 (1229 - 3 inline msg#2)', len(all_blocks) == 1226, str(len(all_blocks)))
check(2, 'message #21 archive fenced = 45', len(archive_blocks[21]) == 45, str(len(archive_blocks[21])))
check(2, 'message #22 archive fenced = 91', len(archive_blocks[22]) == 91, str(len(archive_blocks[22])))
seq_ok, det = True, []
for m in (16, 18, 21, 22):
    lo, hi = SN_RANGES[m]
    hdr = re.search(r'## Message #%d Annex' % m, cs)
    seg = cs[hdr.start():]
    nums = [int(x) for x in re.findall(r'\*\*SN-(\d+)\*\*', seg)]
    nums = [n for n in nums if lo <= n <= hi]
    if nums != list(range(lo, hi + 1)):
        seq_ok = False; det.append('msg%d:%d' % (m, len(nums)))
check(2, 'annex SN sequences complete & ascending (msg#16/18/21/22)', seq_ok, str(det))
# byte-exact annex vs archive for all annex messages
annex_ok, bad = True, []
for m in (3, 5, 8, 10, 12, 14, 16, 18, 21, 22):
    lo, hi = SN_RANGES[m]
    hdr = re.search(r'## Message #%d Annex' % m, cs)
    nxt = re.search(r'## Message #\d+ Annex', cs[hdr.end():])
    seg = cs[hdr.start(): hdr.end() + nxt.start()] if nxt else cs[hdr.start():]
    blocks = fence_re.findall(seg)
    arch = archive_blocks[m]
    if len(blocks) != len(arch) or any(b.rstrip() != a.rstrip() for b, a in zip(blocks, arch)):
        annex_ok = False; bad.append('msg%d %d/%d' % (m, len(blocks), len(arch)))
check(2, 'all annex blocks byte-faithful vs archives (msgs 3..22)', annex_ok, str(bad))

# ---------- 3. Scaffolded documents ----------
specs = sorted(f for f in os.listdir('specs') if f.endswith('.md'))
rfcs = sorted(f for f in os.listdir('rfcs') if f.endswith('.md'))
check(3, 'specs/ = 12 documents', len(specs) == 12, str(len(specs)))
check(3, 'rfcs/ = 55 files', len(rfcs) == 55, str(len(rfcs)))
rfc_docs = [f for f in rfcs if 'ratification' not in f]
records = [f for f in rfcs if 'ratification' in f]
ids = sorted(int(re.match(r'RFC-(\d{4})', f).group(1)) for f in rfc_docs)
check(3, 'RFC-0001..0050 exactly once each', ids == list(range(1, 51)), '%d docs' % len(rfc_docs))
rec_ids = sorted(int(re.match(r'RFC-(\d{4})', f).group(1)) for f in records)
check(3, 'ratification records = 0001, 0002, 0011, 0042, 0049', rec_ids == [1, 2, 11, 42, 49], str(rec_ids))

full_archive = '\n'.join(archive_text[m] for m in [1] + TRANSCRIPT_MSGS)
def norm(s): return '\n'.join(l.rstrip() for l in s.split('\n')).strip()
norm_full = norm(full_archive)
prov_ok, faithful, unfaithful = True, 0, []
for path in ['specs/' + f for f in specs] + ['rfcs/' + f for f in rfcs]:
    t = open(path, encoding='utf-8').read()
    if 'KB-Scaffold Provenance' not in t[:600]:
        prov_ok = False; print('   no provenance header:', path)
    i = t.find('-->')
    body = (t[i+3:] if i >= 0 else t).strip()
    j = body.find('<!-- KB note:')
    if j >= 0: body = body[:j].strip()
    if body in full_archive or norm(body) in norm_full: faithful += 1
    else: unfaithful.append(path)
check(3, 'all 67 scaffolds carry KB provenance headers', prov_ok)
check(3, 'all 67 scaffold bodies verbatim from archive', faithful == 67,
      'faithful=%d missing=%s' % (faithful, unfaithful))

# ---------- 4. Wiki fidelity & provenance ----------
exact = normed = missn = 0
norm_wiki = norm(wiki_all)
for b in all_blocks:
    if b in wiki_all: exact += 1
    elif norm(b) in norm_wiki: normed += 1
    else: missn += 1
check(4, '1226/1226 archived fenced blocks verbatim in Wiki', missn == 0,
      'exact=%d normed=%d missing=%d' % (exact, normed, missn))
prov_pages = [p for p in wiki_pages if re.search(r'^>? ?\*?\*?Provenance|^> Provenance', open(p, encoding='utf-8').read()[:1200], re.M)]
check(4, 'wiki pages with provenance headers (>= 17)', len(prov_pages) >= 17, str(len(prov_pages)))
reps = sorted(glob.glob(f'{KB}/reports/message-*-report.md'))
need = ['message-%03d-report.md' % i for i in range(1, 23)]
have = set(os.path.basename(r) for r in reps)
check(4, 'reports message-001..022 exist', all(n in have for n in need), str(len(reps)))
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

# ---------- 5. Normative consistency (message #21 material) ----------
chain = {34: 'RFC-0033', 35: 'RFC-0034', 36: 'RFC-0035', 37: 'RFC-0036', 38: 'RFC-0037',
         39: 'RFC-0038', 40: 'RFC-0039', 41: 'RFC-0040', 42: 'RFC-0041', 43: 'RFC-0028',
         44: 'RFC-0043', 45: 'RFC-0044', 46: 'RFC-0045', 47: 'RFC-0046', 48: 'RFC-0047',
         49: 'RFC-0048', 50: 'RFC-0049'}
chain_ok, bad = True, []
for n, parent in chain.items():
    f = [x for x in rfc_docs if x.startswith('RFC-%04d-' % n)][0]
    t = open('rfcs/' + f, encoding='utf-8').read()
    m = re.search(r'\*\*Parent:\*\* (RFC-\d{4})', t)
    if not (m and m.group(1) == parent):
        chain_ok = False; bad.append('%04d->%s' % (n, m.group(1) if m else None))
check(5, 'Parent chain RFC-0034..0050 incl. 0043->0028 detour', chain_ok, str(bad))
r46 = open('rfcs/RFC-0046-codp-observability-diagnostics.md', encoding='utf-8').read()
check(5, 'RFC-0046 scaffold cites [196] ratification declaration',
      '[196]' in r46[:800] and 'RATIFIED' in r46[:800])
ri = open(f'{KB}/wiki/RFC-Index.md', encoding='utf-8').read()
rows_ok = True
for n in (43, 44, 45, 47):
    row = re.findall(r'^\| RFC-%04d \|.*$' % n, ri, re.M)
    if not row: rows_ok = False
check(5, 'RFC-Index rows exist for RFC-0043..0047', rows_ok)
row46 = re.findall(r'^\| RFC-0046 \|.*$', ri, re.M)
check(5, 'RFC-Index row RFC-0046 = RATIFIED per [196]', bool(row46) and 'RATIFIED' in row46[0])
check(5, 'ratified set includes RFC-0046', 'RFC-0046 (CODP v1.2, ratified per review declaration [196])' in ri)
check(5, 'no unqualified ratification claims for RFC-0044/0045/0048/0050',
      all(not re.search(r'^\| RFC-00%d \|.*\*\*RATIFIED\*\*' % n, ri, re.M) for n in (44, 45, 48, 50)))
st = open(f'{KB}/wiki/Source-Traceability.md', encoding='utf-8').read()
check(5, 'conflicts C-11 & C-12 recorded', '| C-11 |' in st and '| C-12 |' in st)
check(5, 'duplicates D-64..D-74 recorded', all(('| D-%d |' % d) in st for d in range(64, 75)))
gl = open(f'{KB}/wiki/Glossary.md', encoding='utf-8').read()
terms = ['CSL (RFC-0044)', 'CTDX (RFC-0045)', 'CODP (RFC-0046)', 'CPMWS (RFC-0047)', '**cog**',
         'Lockfile (cog.lock)', 'Observability Conformance Levels', 'Mandatory Replay Traces']
check(5, 'Glossary contains message-#21 terms (8/8)', all(t in gl for t in terms),
      str([t for t in terms if t not in gl]))
terms22 = ['CFFI (RFC-0048)', 'CSTS (RFC-0049)', 'RFC-0050 (capstone)', 'ToolchainManifest',
           'ConformanceManifest', 'Cognitive Epoch', 'FFI Determinism Classes']
check(5, 'Glossary contains message-#22 terms (7/7)', all(x in gl for x in terms22),
      str([x for x in terms22 if x not in gl]))
check(5, 'ObservabilityEvent schema present in Wiki', 'ObservabilityEvent' in wiki_all)

# ---------- 6. RFC parent-chain integrity ----------
no_parent = [f for f in rfc_docs if '**Parent:**' not in open('rfcs/' + f, encoding='utf-8').read()[:1500]]
check(6, 'all 50 RFC documents carry a Parent header', not no_parent, str(no_parent))

# ---------- 7. Status & cross-page coherence ----------
readme = open(f'{KB}/README.md', encoding='utf-8').read()
check(7, 'README totals (22 msgs / 1229 snippets / 12 specs / 55 rfcs)',
      all(s in readme for s in ['22 messages processed', '**1229 code snippets**',
                                '**12 scaffolded documents in `specs/`**', '**55 files in `rfcs/`**']))
cl = open(f'{KB}/wiki/Changelog.md', encoding='utf-8').read()
miss_cl = [i for i in range(1, 23) if ('Message #%d' % i) not in cl]
check(7, 'changelog entries for messages 1..22', not miss_cl, str(miss_cl))

# ---------- 8. Traceability bookkeeping ----------
reg = sorted(set(int(m) for m in re.findall(r'^\| (\d+) \| 2026-', st, re.M)))
check(8, 'register rows 1..22 contiguous', reg == list(range(1, 23)), str(reg))
idx_count = len(re.findall(r'^#{2,3} Message #\d+ sub-message index', st, re.M))
check(8, 'sub-message indexes for msgs 2,3,5,8,10,12,14,16,18,21,22 (11)', idx_count == 11, str(idx_count))
xs = sorted(set(int(m) for m in re.findall(r'^\| X-(\d+) \|', st, re.M)))
check(8, 'cross-references contiguous X-01..X-100', xs == list(range(1, 101)), 'count=%d' % len(xs))
ds = sorted(set(int(m) for m in re.findall(r'^\| D-(\d+) \|', st, re.M)))
check(8, 'duplicate log contiguous D-1..D-74', ds == list(range(1, 75)), 'count=%d' % len(ds))
csids = sorted(set(int(m) for m in re.findall(r'^\| C-(\d+) \|', st, re.M)))
check(8, 'conflict log contiguous C-1..C-12', csids == list(range(1, 13)), str(csids))
mandated = ['specs', 'rfcs', 'compiler', 'runtime', 'dialects', 'cognition', 'tests', 'examples', 'docs']
check(8, 'RC-000 section 8 mandated directories exist (9/9)', all(os.path.isdir(d) for d in mandated))

fails = [r for r in results if not r[2]]
bycat = {}
for c, n, ok, d in results:
    bycat.setdefault(c, [0, 0]); bycat[c][1] += 1
    if ok: bycat[c][0] += 1
print('\nPer-category:', {c: '%d/%d' % tuple(v) for c, v in sorted(bycat.items())})
print('%d/%d checks passed' % (len(results) - len(fails), len(results)))
sys.exit(1 if fails else 0)
