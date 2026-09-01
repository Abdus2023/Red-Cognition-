#!/usr/bin/env python3
"""
common.py — dependency bootstrap for acquisition stages.
Session-ephemeral state (clones in /tmp, extracted trees in artifacts/derived/)
is re-created on demand from committed originals + GitHub. Nothing else is
trusted: everything derived comes from committed tarballs (whose hashes are in
artifacts/manifests/sha256sums.txt) or fresh pinned git operations.
"""
import os, subprocess, tarfile

ROOT = "/home/user/Red-Cognition-"
ACQ = "/tmp/acq"

CLONES = [
    ("red", "https://github.com/red/red.git"),
    ("rebol_rebol", "https://github.com/rebol/rebol.git"),
    ("rebolsource_r3", "https://github.com/rebolsource/r3.git"),
    ("metaeducation_ren-c", "https://github.com/metaeducation/ren-c.git"),
    ("Oldes_Rebol3", "https://github.com/Oldes/Rebol3.git"),
    ("rebolsource_rebol-syntax", "https://github.com/rebolsource/rebol-syntax.git"),
    ("rebolsource_rebol-test", "https://github.com/rebolsource/rebol-test.git"),
]

EXTRACTS = [
    ("red-0.6.6", "artifacts/red/releases/red-0.6.6.tar.gz"),
    ("red-0.6.4", "artifacts/red/releases/red-0.6.4.tar.gz"),
    ("rebol-rebol-25033f897", "artifacts/rebol/source/rebol-rebol-25033f897.tar.gz"),
    ("ren-c-e31d5698d", "artifacts/rebol/source/ren-c-e31d5698d.tar.gz"),
    ("rebolsource-r3-98cdfcd6e", "artifacts/rebol/source/rebolsource-r3-98cdfcd6e.tar.gz"),
    ("Oldes-Rebol3-d5b237cea", "artifacts/rebol/source/Oldes-Rebol3-d5b237cea.tar.gz"),
    ("rebol-syntax-4ff113963", "artifacts/rebol/documentation/rebol-syntax-4ff113963.tar.gz"),
    ("rebol-test-409ef5c22", "artifacts/rebol/tests/rebol-test-409ef5c22.tar.gz"),
]

def ensure_clones():
    for name, url in CLONES:
        d = os.path.join(ACQ, name)
        if not os.path.isdir(os.path.join(d, ".git")):
            subprocess.run(["git", "clone", "--quiet", "--filter=blob:none",
                            "--no-checkout", url, d], check=True)

def ensure_extracts():
    der = os.path.join(ROOT, "artifacts", "derived", "extracted")
    for name, arel in EXTRACTS:
        dest = os.path.join(der, name)
        if not os.path.isdir(dest) or not os.listdir(dest):
            os.makedirs(dest, exist_ok=True)
            with tarfile.open(os.path.join(ROOT, arel)) as tf:
                tf.extractall(dest)

def top_dir(extract_name):
    base = os.path.join(ROOT, "artifacts", "derived", "extracted", extract_name)
    entries = [e for e in os.listdir(base) if not e.startswith(".")]
    return os.path.join(base, entries[0]) if len(entries) == 1 else base

def ensure_deps():
    ensure_clones()
    ensure_extracts()
