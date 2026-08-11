#!/usr/bin/env python3
"""Message #29 final verification suite for the Red-Cognition knowledge base.
Run from the repository root: python3 knowledge-base/reports/message-029-verification-suite.py
Corpus scope: KB messages 1..29 processed, sub-messages [1]..[320], SN-001..SN-1975,
12 specs + 84 rfcs scaffolded files (96 scaffolds)."""
import re, glob, os, sys

KB = 'knowledge-base'
results = []
def check(cat, name, ok, detail=''):
    results.append((cat, name, bool(ok), detail))
    print(('PASS' if ok else 'FAIL'), '[%s]' % cat, name, ('| ' + detail if detail else ''))

fence_re = re.compile(r'^[^\S\n]*```[^\n]*\n(.*?)^[^\S\n]*```[^\n]*$', re.M | re.S)

TRANSCRIPT_MSGS = [2, 3, 5, 8, 10, 12, 14, 16, 18, 21, 22, 23, 25, 26, 27, 29]
MSG_PARTS = {2: 2, 3: 4, 5: 5, 8: 5, 10: 5, 12: 5, 14: 5, 16: 5, 18: 5, 21: 5, 22: 5, 23: 5, 25: 5, 26: 5, 27: 5, 29: 5}
EXPECTED_RANGES = {2: (1, 20), 3: (21, 40), 5: (41, 60), 8: (61, 80), 10: (81, 100),
                   12: (101, 120), 14: (121, 140), 16: (141, 160), 18: (161, 180),
                   21: (181, 200), 22: (201, 220), 23: (221, 240), 25: (241, 260), 26: (261, 280), 27: (281, 300), 29: (301, 320)}
SN_RANGES = {2: (1, 123), 3: (124, 212), 5: (213, 318), 8: (319, 427), 10: (428, 493),
             12: (494, 640), 14: (641, 825), 16: (826, 993), 18: (994, 1093),
             21: (1094, 1138), 22: (1139, 1229), 23: (1230, 1348), 25: (1349, 1419), 26: (1420, 1591), 27: (1592, 1777), 29: (1778, 1975)}
# fenced blocks per message = total snippets minus inline (msg#2: SN-001/002/003 inline)
FENCED = {2: 120, 3: 89, 5: 106, 8: 109, 10: 66, 12: 147, 14: 185, 16: 168, 18: 100,
          21: 45, 22: 91, 23: 119, 25: 71, 26: 172, 27: 186, 29: 198}

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
st = open(f'{KB}/wiki/Source-Traceability.md', encoding='utf-8').read()
ri = open(f'{KB}/wiki/RFC-Index.md', encoding='utf-8').read()
gl = open(f'{KB}/wiki/Glossary.md', encoding='utf-8').read()
cl = open(f'{KB}/wiki/Changelog.md', encoding='utf-8').read()
readme = open(f'{KB}/README.md', encoding='utf-8').read()

# ---------- 1. Archive structure ----------
missing = [f for m in [1] + TRANSCRIPT_MSGS for f in archive_files(m) if not os.path.exists(f)]
check(1, 'all archive files exist (78 files)', not missing, str(missing))
labels, speaker_ok = [], True
for m in TRANSCRIPT_MSGS:
    for mm in re.finditer(r'^## \[(\d+)\] ?(.*)$', archive_text[m], re.M):
        labels.append(int(mm.group(1)))
        if not mm.group(2).strip(): speaker_ok = False
check(1, 'sub-message labels [1]..[320] contiguous (320/320)', labels == list(range(1, 321)), 'count=%d' % len(labels))
check(1, 'every sub-message header carries a speaker label', speaker_ok)

# ---------- 2. Snippet-ledger integrity ----------
tok_ok, miss = True, []
for i in range(1, 1976):
    tok = 'SN-%03d' % i if i < 1000 else 'SN-%d' % i
    if not re.search(r'(?<![0-9A-Z-])' + tok + r'(?!\d)', cs):
        tok_ok = False; miss.append(tok)
check(2, 'SN-001..SN-1975 all present in Code-Snippets', tok_ok, str(miss[:5]))
tot = re.search(r'\*\*Corpus totals: (\d+) snippets\*\*', cs)
check(2, 'Code-Snippets corpus totals line = 1975', tot and tot.group(1) == '1975', tot.group(1) if tot else 'missing')
tot_line = [l for l in cs.split('\n') if l.startswith('**Corpus totals:')][0]
check(2, 'totals line has exactly one parenthetical breakdown (no duplicate residue)',
      tot_line.count('). (') == 0 and tot_line.endswith('Message #29 Annex at the bottom of this page).'),
      'paren-groups=%d' % tot_line.count('). ('))
ledger_rows = re.findall(r'^\| (SN-\d{3}) \|', cs, re.M)
check(2, 'message #2 ledger has 123 rows', len(ledger_rows) == 123, str(len(ledger_rows)))
for m in (16, 18, 21, 22, 23, 25, 26, 27, 29):
    bt = re.search(r'Message #%d breakdown:(.*?)(?=Message #\d+ breakdown:|Note:|## |\Z)' % m, cs, re.S)
    rows = re.findall(r'\| \[(\d+)\] \| (\d+) \|', bt.group(1)) if bt else []
    lo, hi = EXPECTED_RANGES[m]
    exp = SN_RANGES[m][1] - SN_RANGES[m][0] + 1
    ok = len(rows) == hi - lo + 1 and sum(int(r[1]) for r in rows) == exp and all(lo <= int(r[0]) <= hi for r in rows)
    check(2, 'message #%d breakdown table (%d rows, sum %d)' % (m, hi-lo+1, exp), ok,
          'rows=%d sum=%d' % (len(rows), sum(int(r[1]) for r in rows)))
check(2, 'archive fenced total = 1972 (1975 - 3 inline msg#2)', len(all_blocks) == 1972, str(len(all_blocks)))
fenced_ok, fdet = True, []
for m in TRANSCRIPT_MSGS:
    if len(archive_blocks[m]) != FENCED[m]:
        fenced_ok = False; fdet.append('msg%d:%d!=%d' % (m, len(archive_blocks[m]), FENCED[m]))
check(2, 'per-message fenced counts = breakdown sums (all 16 transcript messages)', fenced_ok, str(fdet))
seq_ok, det = True, []
for m in (16, 18, 21, 22, 23, 25, 26, 27, 29):
    lo, hi = SN_RANGES[m]
    hdr = re.search(r'## Message #%d Annex' % m, cs)
    seg = cs[hdr.start():]
    nums = [int(x) for x in re.findall(r'\*\*SN-(\d+)\*\*', seg)]
    nums = [n for n in nums if lo <= n <= hi]
    if nums != list(range(lo, hi + 1)):
        seq_ok = False; det.append('msg%d:%d' % (m, len(nums)))
check(2, 'annex SN sequences complete & ascending (msg#16/18/21/22/23/25/26/27/29)', seq_ok, str(det))
annex_ok, bad = True, []
for m in (3, 5, 8, 10, 12, 14, 16, 18, 21, 22, 23, 25, 26, 27, 29):
    hdr = re.search(r'## Message #%d Annex' % m, cs)
    nxt = re.search(r'## Message #\d+ Annex', cs[hdr.end():])
    seg = cs[hdr.start(): hdr.end() + nxt.start()] if nxt else cs[hdr.start():]
    blocks = fence_re.findall(seg)
    arch = archive_blocks[m]
    if len(blocks) != len(arch) or any(b.rstrip() != a.rstrip() for b, a in zip(blocks, arch)):
        annex_ok = False; bad.append('msg%d %d/%d' % (m, len(blocks), len(arch)))
check(2, 'all annex blocks byte-faithful vs archives (msgs 3..29, 1972 blocks)', annex_ok, str(bad))

# ---------- 3. Scaffolded documents ----------
specs = sorted(f for f in os.listdir('specs') if f.endswith('.md'))
rfcs = sorted(f for f in os.listdir('rfcs') if f.endswith('.md'))
check(3, 'specs/ = 12 documents', len(specs) == 12, str(len(specs)))
check(3, 'rfcs/ = 84 files', len(rfcs) == 84, str(len(rfcs)))
rfc_docs = [f for f in rfcs if 'ratification' not in f]
records = [f for f in rfcs if 'ratification' in f]
ids = sorted(int(re.match(r'RFC-(\d{4})', f).group(1)) for f in rfc_docs)
check(3, 'RFC-0001..0071 exactly once each', ids == list(range(1, 72)), '%d docs' % len(rfc_docs))
rec_ids = sorted(int(re.match(r'RFC-(\d{4})', f).group(1)) for f in records)
check(3, 'ratification records = 0001, 0002, 0011, 0042, 0049, 0050, 0052, 0053, 0057, 0058, 0059, 0060, 0061',
      rec_ids == [1, 2, 11, 42, 49, 50, 52, 53, 57, 58, 59, 60, 61], str(rec_ids))
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
check(3, 'all 96 scaffolds carry KB provenance headers', prov_ok)
check(3, 'all 96 scaffold bodies verbatim from archive', faithful == 96,
      'faithful=%d missing=%s' % (faithful, unfaithful))

# ---------- 4. Wiki fidelity & provenance ----------
exact = normed = missn = 0
norm_wiki = norm(wiki_all)
for b in all_blocks:
    if b in wiki_all: exact += 1
    elif norm(b) in norm_wiki: normed += 1
    else: missn += 1
check(4, '1972/1972 archived fenced blocks verbatim in Wiki', missn == 0,
      'exact=%d normed=%d missing=%d' % (exact, normed, missn))
prov_pages = [p for p in wiki_pages if re.search(r'^>? ?\*?\*?Provenance|^> Provenance', open(p, encoding='utf-8').read()[:1200], re.M)]
check(4, 'wiki pages with provenance headers (>= 17)', len(prov_pages) >= 17, str(len(prov_pages)))
reps = sorted(glob.glob(f'{KB}/reports/message-*-report.md'))
need = ['message-%03d-report.md' % i for i in range(1, 30)]
have = set(os.path.basename(r) for r in reps)
check(4, 'reports message-001..029 exist', all(n in have for n in need), str(len(reps)))
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

# ---------- 5. Normative consistency (message-#29 material) ----------
def scaffold(n):
    f = [x for x in rfc_docs if x.startswith('RFC-%04d-' % n)][0]
    return open('rfcs/' + f, encoding='utf-8').read()
rec61 = open('rfcs/RFC-0061-ratification-record.md', encoding='utf-8').read()
check(5, 'RFC-0061 ratification record: formal record sourced from [301] (Status Ratified + hereby ratified; D-95/C-17 noted)',
      '**Status:** **Ratified**' in rec61 and 'is hereby ratified as a normative specification' in rec61
      and '[301]' in rec61[:1600] and 'D-95' in rec61[:1600] and 'C-17' in rec61[:1600])
r62 = scaffold(62)
check(5, 'RFC-0062 scaffold v1.1 per [304]: Candidate for Final Ratification + CVMX + READY FOR RATIFICATION',
      'Candidate for Final Ratification' in r62[:1800] and 'CVMX' in r62 and 'READY FOR RATIFICATION' in r62)
check(5, 'RFC-0062 provenance: D-94 + C-18 + supersession of [288]/[302]/[303] noted; no ratification decision',
      'D-94' in r62[:1600] and 'C-18' in r62[:1600] and 'No ratification decision present in corpus' in r62[:1600])
r63 = scaffold(63)
check(5, 'RFC-0063 scaffold v1.1 per [306]: Candidate + LTS/step semantics + no ratification decision',
      'Candidate for Final Ratification' in r63[:1800] and 'READY FOR RATIFICATION' in r63
      and 'No ratification decision present in corpus' in r63[:1600])
r64 = scaffold(64)
check(5, 'RFC-0064 scaffold v1.0 per [307]: Draft + [308] v1.1 recommendation noted',
      'v1.0 (Draft)' in r64[:1600] and '[308]' in r64[:1600])
r65 = scaffold(65)
check(5, 'RFC-0065 scaffold v1.0 per [309]: Draft + CPCPF acronym/RFC-0033 + parent quirk noted',
      'v1.0 (Draft)' in r65[:1800] and 'RFC-0033' in r65[:1800] and 'quirk preserved' in r65[:1800])
r66 = scaffold(66)
check(5, 'RFC-0066 scaffold v1.0 per [311]: Draft + RFC-0034 CPR-TDP relationship noted',
      'v1.0 (Draft)' in r66[:1600] and 'CPR-TDP' in r66[:1600])
r67 = scaffold(67)
check(5, 'RFC-0067 scaffold v1.0 per [313]: Draft + RFC-0047 CPMWS overlap noted',
      'v1.0 (Draft)' in r67[:1800] and 'RFC-0047' in r67[:1800])
r68 = scaffold(68)
check(5, 'RFC-0068 scaffold v1.0 per [314] (CHATGPT): Draft + C-11 roadmap divergence noted',
      'v1.0 (Draft)' in r68[:1800] and 'C-11' in r68[:1800] and 'CHATGPT-authored' in r68[:1800])
r69 = scaffold(69)
check(5, 'RFC-0069 scaffold v1.0 per [315]: Draft + [316] v1.1 recommendations noted',
      'v1.0 (Draft)' in r69[:1600] and '[316]' in r69[:1600])
r70 = scaffold(70)
check(5, 'RFC-0070 scaffold v1.0 per [317]: Draft + [318] review noted',
      'v1.0 (Draft)' in r70[:1600] and '[318]' in r70[:1600])
r71 = scaffold(71)
check(5, 'RFC-0071 scaffold v1.0 per [319]: Draft + [320] review + [316] naming divergence noted',
      'v1.0 (Draft)' in r71[:1800] and '[320]' in r71[:1800] and 'C-11' in r71[:1800])
row_ok = True
for n in (62, 63, 64, 65, 66, 67, 68, 69, 70, 71):
    rows = re.findall(r'^\| RFC-%04d \|.*$' % n, ri, re.M)
    if not rows: row_ok = False
check(5, 'RFC-Index rows exist for RFC-0062..0071', row_ok)
check(5, 'no ratification claims for RFC-0062..0071 rows',
      all(not any('RATIFIED' in r for r in re.findall(r'^\| RFC-%04d \|.*$' % n, ri, re.M)) for n in range(62, 72)))
check(5, 'ratified set unchanged after message #29 (RFC-0061 row still RATIFIED; section present)',
      any('RATIFIED' in r for r in re.findall(r'^\| RFC-0061 \|.*$', ri, re.M))
      and 'Ratified set after message #29' in ri)
check(5, 'conflicts C-17 and C-18 recorded', '| C-17 |' in st and '| C-18 |' in st)
check(5, 'duplicates D-94 and D-95 recorded', '| D-94 |' in st and '| D-95 |' in st)
check(5, 'cross-references X-122..X-133 present', all(('| X-%d |' % x) in st for x in range(122, 134)))
terms29 = ['CVMX', 'ModuleIdentity', 'CVM-FOS (RFC-0063)', 'CCC-VTP (RFC-0064)', 'CPCPF (RFC-0065)',
           'ArtifactTrustLevel', 'CPRDP (RFC-0066)', 'PackageID (CPRDP)', 'CPM-WS (RFC-0067)',
           'CBS-RAP (RFC-0068)', 'BuildReceipt', 'CRDLMP (RFC-0069)', 'CognitiveDeploymentUnit',
           'LifecycleState (CRDLMP)', 'CROFP (RFC-0070)', 'CRCP (RFC-0071)']
check(5, 'Glossary contains message-#29 terms (16/16) and CVMB annotated with C-18',
      all(x in gl for x in terms29) and 'divergence C-18' in gl, str([x for x in terms29 if x not in gl]))

# ---------- 6. RFC parent-chain integrity ----------
no_parent = [f for f in rfc_docs if '**Parent:**' not in open('rfcs/' + f, encoding='utf-8').read()[:1500]]
check(6, 'all 71 RFC documents carry a Parent header', not no_parent, str(no_parent))
chain = {34: 'RFC-0033', 35: 'RFC-0034', 36: 'RFC-0035', 37: 'RFC-0036', 38: 'RFC-0037',
         39: 'RFC-0038', 40: 'RFC-0039', 41: 'RFC-0040', 42: 'RFC-0041', 43: 'RFC-0028',
         44: 'RFC-0043', 45: 'RFC-0044', 46: 'RFC-0045', 47: 'RFC-0046', 48: 'RFC-0047',
         49: 'RFC-0048', 50: 'RFC-0049', 51: 'RFC-0050', 52: 'RFC-0051', 53: 'RFC-0052',
         54: 'RFC-0053', 55: 'RFC-0054', 56: 'RFC-0055',
         57: 'RFC-0056', 58: 'RFC-0057', 59: 'RFC-0058', 60: 'RFC-0059', 61: 'RFC-0060', 62: 'RFC-0061',
         63: 'RFC-0062', 64: 'RFC-0063', 65: 'RFC-0064', 66: 'RFC-0065', 67: 'RFC-0066',
         68: 'RFC-0067', 69: 'RFC-0068', 70: 'RFC-0069', 71: 'RFC-0070'}
chain_ok, badc = True, []
for n, parent in chain.items():
    d = scaffold(n)
    m = re.search(r'\*\*Parent:\*\* (RFC-\d{4})', d)
    if not (m and m.group(1) == parent):
        chain_ok = False; badc.append('%04d->%s' % (n, m.group(1) if m else None))
check(6, 'documented parent chain RFC-0034..0071 exact (incl. 0043->0028 detour)', chain_ok, str(badc))

# ---------- 7. Status & cross-page coherence ----------
check(7, 'README: 29 messages processed; current totals (1975 / 12 specs / 84 rfcs)',
      '29 messages processed' in readme and all(s in readme for s in [
          '**1975 code snippets**', '**12 scaffolded documents in `specs/`**', '**84 files in `rfcs/`**']))
check(7, 'README: no stale messages-processed counts (26/27/28) remain',
      all(('%d messages processed' % n) not in readme for n in (26, 27, 28)))
check(7, 'README: message ordering #27 -> #28 -> #29 with totals ascending',
      readme.index('Message #27 = ') < readme.index('Message #28 = ') < readme.index('Message #29 = ')
      and readme.index('**1777 code snippets**') < readme.index('**1975 code snippets**'))
check(7, 'README Code Snippets table row current (1975 snippets, SN-001…SN-1975)',
      'ledger of all 1975 snippets (SN-001…SN-1975)' in readme and 'ledger of all 1777 snippets' not in readme)
check(7, 'Code-Snippets provenance header current (covers messages #2..#29)',
      '#26, #27, #29' in cs[:700] and 'message-029-part1..5' in cs[:1100])
miss_cl = [i for i in range(1, 30) if ('Message #%d' % i) not in cl]
check(7, 'changelog entries for messages 1..29', not miss_cl, str(miss_cl))

# ---------- 8. Traceability bookkeeping ----------
reg = sorted(set(int(m) for m in re.findall(r'^\| (\d+) \| 2026-', st, re.M)))
check(8, 'register rows 1..29 contiguous', reg == list(range(1, 30)), str(reg))
idx_count = len(re.findall(r'^#{2,3} Message #\d+ sub-message index', st, re.M))
check(8, 'sub-message indexes for the 16 transcript messages', idx_count == 16, str(idx_count))
xs = sorted(set(int(m) for m in re.findall(r'^\| X-(\d+) \|', st, re.M)))
check(8, 'cross-references contiguous X-01..X-133', xs == list(range(1, 134)), 'count=%d' % len(xs))
ds = sorted(set(int(m) for m in re.findall(r'^\| D-(\d+) \|', st, re.M)))
check(8, 'duplicate log contiguous D-1..D-95', ds == list(range(1, 96)), 'count=%d' % len(ds))
csids = sorted(set(int(m) for m in re.findall(r'^\| C-(\d+) \|', st, re.M)))
check(8, 'conflict log contiguous C-1..C-18', csids == list(range(1, 19)), str(csids))
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
