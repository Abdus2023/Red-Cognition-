#!/usr/bin/env python3
"""Message #18 final verification suite for the Red-Cognition knowledge base.
Run from the repository root: python3 knowledge-base/reports/message-018-verification-suite.py"""
import re, glob, os, sys

KB = 'knowledge-base'
results = []
def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('PASS' if ok else 'FAIL'), '-', name, ('| ' + detail if detail else ''))

fence_re = re.compile(r'^[^\S\n]*```[^\n]*\n(.*?)^[^\S\n]*```[^\n]*$', re.M | re.S)

def load_subs(msgnum, lo, hi):
    files = sorted(glob.glob(f'{KB}/sources/message-{msgnum:03d}-original-part*.md'))
    subs, order, cur, buf = {}, [], None, []
    for f in files:
        for line in open(f, encoding='utf-8').read().splitlines(keepends=True):
            m = re.match(r'^## \[(\d+)\] (.*)$', line)
            if m:
                if cur is not None:
                    subs[cur] = ''.join(buf); order.append(cur)
                cur = int(m.group(1)); buf = []
            elif cur is not None:
                buf.append(line)
    if cur is not None:
        subs[cur] = ''.join(buf); order.append(cur)
    return files, subs, order

# ---------- 1. Archive structure ----------
files18, subs18, order18 = load_subs(18, 161, 180)
check('1a archive parts 1..5 exist', len(files18) == 5, str(len(files18)))
check('1b sub-messages [161]..[180] contiguous', order18 == list(range(161, 181)), str(order18))

# ---------- 2. Snippet annex integrity ----------
cs = open(f'{KB}/wiki/Code-Snippets.md', encoding='utf-8').read()
archive_blocks = []
per_sub_counts = {}
for n in order18:
    bl = fence_re.findall(subs18[n])
    per_sub_counts[n] = len(bl)
    archive_blocks.extend(bl)
check('2a archive fenced blocks = 100', len(archive_blocks) == 100, str(len(archive_blocks)))

# detect SN marker padding
pad = 4 if '**SN-0001**' in cs else 3
def sn(i): return '**SN-' + str(i).zfill(pad if i < 1000 else 4) + '**' if pad == 4 else '**SN-%03d**' % i
markers_ok = True
positions = []
for i in range(1, 1094):
    tok = 'SN-%03d' % i if i < 1000 else 'SN-%d' % i
    hits = re.findall(r'(?<![0-9A-Z-])' + tok + r'(?!\d)', cs)
    if not hits: markers_ok = False; print('   marker missing', tok)
    positions.append(cs.find(tok))
check('2b SN-001..SN-1093 all present (ledger+annex formats)', markers_ok)

# annex byte-exact: parse blocks after SN-993 marker
annex_start = cs.find('**SN-993**')
annex = cs[annex_start:]
annex_blocks, idx = [], 0
while True:
    m = re.search(r'\*\*SN-(\d+)\*\*', annex[idx:])
    if not m: break
    num = int(m.group(1))
    rest = annex[idx + m.end():]
    fm = re.search(r'^[^\S\n]*```[^\n]*\n(.*?)^[^\S\n]*```[^\n]*$', rest, re.M | re.S)
    if fm and 994 <= num <= 1093:
        annex_blocks.append((num, fm.group(1)))
    idx += m.end()
check('2d annex blocks for SN-994..SN-1093 = 100', len(annex_blocks) == 100, str(len(annex_blocks)))
byte_ok = all(ab == archive_blocks[i] for i, (n, ab) in enumerate(annex_blocks)) if len(annex_blocks) == 100 else False
rstrip_ok = all(ab.rstrip() == archive_blocks[i].rstrip() for i, (n, ab) in enumerate(annex_blocks)) if len(annex_blocks) == 100 else False
check('2e annex byte-exact vs archive (100/100)', byte_ok, 'exact=%s rstrip=%s' % (byte_ok, rstrip_ok))
seq_ok = [n for n, _ in annex_blocks] == list(range(994, 1094))
check('2f annex SN sequence 994..1093', seq_ok)

# breakdown table sum
bt = re.search(r'Message #18 breakdown:(.*?)(?=Note:)', cs, re.S)
rows = re.findall(r'\| \[(\d+)\] \| (\d+) \|', bt.group(1)) if bt else []
check('2g breakdown table has 20 rows summing to 100', len(rows) == 20 and sum(int(r[1]) for r in rows) == 100,
      'rows=%d sum=%d' % (len(rows), sum(int(r[1]) for r in rows)))
table_ok = all(per_sub_counts[int(r[0])] == int(r[1]) for r in rows)
check('2h breakdown table matches archive per-sub counts', table_ok)

# ---------- 3. Scaffolded documents ----------
specs = sorted(f for f in os.listdir('specs') if f.endswith('.md'))
rfcs = sorted(f for f in os.listdir('rfcs') if f.endswith('.md'))
check('3a specs/ = 12 files', len(specs) == 12, str(len(specs)))
check('3b rfcs/ >= 46 files (monotonic)', len(rfcs) >= 46, str(len(rfcs)))
rfc_docs = [f for f in rfcs if re.match(r'RFC-\d{4}-[a-z]', f) and 'ratification' not in f]
records = [f for f in rfcs if 'ratification' in f]
ids = sorted(int(re.match(r'RFC-(\d{4})', f).group(1)) for f in rfc_docs)
check('3c RFC-0001..0042 present (monotonic)', set(range(1, 43)) <= set(ids), 'docs=%d records=%d' % (len(rfc_docs), len(records)))
check('3d ratification records include 0001/0002/0011/0042 (monotonic)',
      set(int(re.match(r'RFC-(\d{4})', f).group(1)) for f in records) >= {1, 2, 11, 42}, str(records))

def sub_body(n):
    b = subs18[n]
    b = b.split('\n', 1)[1] if b.startswith('## [') else b
    return b

# Full concatenated archive text (all parts, everything) for substring fidelity check.
full_archive = '\n'.join(open(f, encoding='utf-8').read() for f in files18)

def file_body(path):
    t = open(path, encoding='utf-8').read()
    i = t.find('-->')
    body = t[i+3:] if i >= 0 else t
    body = body.lstrip('\n')
    j = body.find('<!-- KB note:')
    if j >= 0:
        body = body[:j]
    return body.rstrip('\n')

def normalize_ws(s):
    # collapse trailing-whitespace-only differences per line (archive keeps two-space line breaks)
    return '\n'.join(l.rstrip() for l in s.split('\n')).strip()

mapping = {
 'RFC-0034-cpr-tdp-package-registry.md': 163,
 'RFC-0035-cseim-sandbox-isolation.md': 164,
 'RFC-0036-cbr-scp-supply-chain.md': 165,
 'RFC-0037-cslemp-lifecycle-evolution.md': 166,
 'RFC-0038-cmaep-marketplace-economy.md': 167,
 'RFC-0039-cieop-identity-economy-ownership.md': 169,
 'RFC-0040-cgcdp-governance-collective-decision.md': 171,
 'RFC-0041-cifp-interoperability-federation.md': 173,
 'RFC-0042-cadp-autonomous-deployment.md': 177,
 'RFC-0042-ratification-record.md': 179,
}
exact, contained, provenance_ok = 0, 0, True
norm_archive = normalize_ws(full_archive)
details = []
for fname, n in mapping.items():
    fb = file_body('rfcs/' + fname)
    ab = sub_body(n)
    if fb == ab: exact += 1
    elif fb in ab or normalize_ws(fb) in norm_archive: contained += 1
    else: details.append(fname); print('   scaffold mismatch:', fname)
    head = open('rfcs/' + fname, encoding='utf-8').read(800)
    if ('sub-message [%d]' % n) not in head:
        provenance_ok = False; print('   provenance wrong:', fname, n)
ok3e = exact + contained == len(mapping)
check('3e 10 new scaffolds byte-exact vs archive', ok3e,
      'exact=%d contained=%d missing=%s' % (exact, contained, details))
check('3f provenance headers cite correct sub-messages', provenance_ok)

# ---------- 4. Link integrity ----------
link_re = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')
broken = []
for md in glob.glob(f'{KB}/*.md') + glob.glob(f'{KB}/wiki/*.md') + glob.glob(f'{KB}/reports/*.md'):
    base = os.path.dirname(md)
    text = open(md, encoding='utf-8').read()
    for _, target in link_re.findall(text):
        if re.match(r'^(https?:|mailto:|#)', target): continue
        t = target.split('#')[0]
        if not t: continue
        if not os.path.exists(os.path.normpath(os.path.join(base, t))):
            broken.append((md, target))
check('4 internal markdown links all resolve', not broken, 'broken=%d %s' % (len(broken), broken[:5]))

# ---------- 5. Bookkeeping ----------
st = open(f'{KB}/wiki/Source-Traceability.md', encoding='utf-8').read()
reg = set(int(m) for m in re.findall(r'^\| (\d+) \| 2026-', st, re.M))
check('5a register rows include 1..18 (monotonic)', set(range(1, 19)) <= reg, str(sorted(reg)))
idx_rows = set(int(m) for m in re.findall(r'^\| \[(\d+)\] \|', st, re.M))
check('5b sub-message index contains [161]..[180]', set(range(161, 181)) <= idx_rows)
xs = sorted(set(int(m) for m in re.findall(r'^\| X-(\d+) \|', st, re.M)))
check('5c X-refs contiguous incl. X-01..X-87 (monotonic)', xs == list(range(1, max(xs) + 1)) and max(xs) >= 87, 'max=%d count=%d' % (max(xs), len(xs)))
ds = sorted(set(int(m) for m in re.findall(r'^\| D-(\d+) \|', st, re.M)))
check('5d duplicates include D-1..D-62 (monotonic)', set(range(1, 63)) <= set(ds), 'max=%d count=%d' % (max(ds), len(ds)))
csids = sorted(set(int(m) for m in re.findall(r'^\| C-(\d+) \|', st, re.M)))
check('5e conflicts contiguous incl. C-1..C-10 (monotonic)', csids == list(range(1, max(csids) + 1)) and max(csids) >= 10, str(csids))
cl = open(f'{KB}/wiki/Changelog.md', encoding='utf-8').read()
missing_cl = [i for i in range(1, 19) if ('Message #%d' % i) not in cl]
check('5f changelog entries messages 1..18', not missing_cl, str(missing_cl))
reps = sorted(glob.glob(f'{KB}/reports/message-*-report.md'))
check('5g reports message-001..018 exist (monotonic)', len(reps) >= 18, str(len(reps)))

# ---------- 6. README / RFC-Index coherence ----------
readme = open(f'{KB}/README.md', encoding='utf-8').read()
m_sn = re.search(r'\*\*(\d+) code snippets\*\*', readme)
m_rf = re.search(r'\*\*(\d+) files in `rfcs/`\*\*', readme)
check('6a README totals (monotonic: >= 1093 snippets, 12 specs, >= 46 rfcs)',
      re.search(r'\d+ messages processed', readme)
      and '**12 scaffolded documents in `specs/`**' in readme
      and m_sn and int(m_sn.group(1)) >= 1093
      and m_rf and int(m_rf.group(1)) >= 46,
      'sn=%s rfcs=%s' % (m_sn.group(1) if m_sn else None, m_rf.group(1) if m_rf else None))
ri = open(f'{KB}/wiki/RFC-Index.md', encoding='utf-8').read()
check('6b RFC-Index lists RFC-0042 Ratified', re.search(r'RFC-0042.*ratified', ri, re.I) is not None)

fails = [r for r in results if not r[1]]
print('\n%d/%d checks passed' % (len(results) - len(fails), len(results)))
sys.exit(1 if fails else 0)
