#!/usr/bin/env python3
"""
Stage 01 — Source discovery (GitHub API).
Every query is logged with timestamp, status and outcome classification.
Nothing is inferred: failures are recorded as failures.
Output: artifacts/manifests/github-discovery.json
"""
import json, os, subprocess, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "artifacts")
MAN = os.path.join(ART, "manifests")
LOGS = os.path.join(ART, "logs")
QUERIES_LOG = os.path.join(LOGS, "search-queries.log")
NET_LOG = os.path.join(LOGS, "network-events.log")

TOKEN = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()

def log_query(kind, query, status, detail=""):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "tool": "01_discover.py", "kind": kind, "query": query,
           "status": status, "detail": detail}
    with open(QUERIES_LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")

def log_net(url, status, detail=""):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "url": url, "http_status": status, "detail": detail}
    with open(NET_LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")

def gh_json(url):
    """GET a GitHub API URL. Returns (http_status, data_or_none)."""
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "rebol-red-acquisition-agent/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            log_net(url, r.status)
            return r.status, json.loads(body)
    except urllib.error.HTTPError as e:
        log_net(url, e.code, e.reason)
        return e.code, None
    except Exception as e:
        log_net(url, "ERROR", str(e))
        return None, None

results = {"collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "repositories": {}, "searches": {}, "failures": []}

def collect_repo(owner_repo, with_tags=False, with_releases=False):
    st, data = gh_json(f"https://api.github.com/repos/{owner_repo}")
    entry = {"requested": owner_repo}
    if st == 200 and data:
        entry.update({
            "status": "OK",
            "url": data.get("html_url"),
            "owner": (data.get("owner") or {}).get("login"),
            "name": data.get("name"),
            "full_name": data.get("full_name"),
            "default_branch": data.get("default_branch"),
            "description": data.get("description"),
            "license": (data.get("license") or {}).get("spdx_id"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "fork": data.get("fork"),
            "parent": (data.get("parent") or {}).get("full_name"),
            "archived": data.get("archived"),
            "created_at": data.get("created_at"),
            "pushed_at": data.get("pushed_at"),
            "open_issues": data.get("open_issues_count"),
        })
    else:
        entry["status"] = {404: "NOT_FOUND", 403: "RATE_LIMITED",
                           401: "AUTH_REQUIRED"}.get(st, "FETCH_FAILED")
        entry["http_status"] = st
        results["failures"].append({"url": f"repos/{owner_repo}", "http_status": st})
    if with_tags and entry.get("status") == "OK":
        st2, tags = gh_json(f"https://api.github.com/repos/{owner_repo}/tags?per_page=100")
        entry["tags"] = [t.get("name") for t in tags] if st2 == 200 and tags else None
        if tags and len(tags) == 100:
            st2b, tags2 = gh_json(f"https://api.github.com/repos/{owner_repo}/tags?per_page=100&page=2")
            if st2b == 200 and tags2:
                entry["tags"] += [t.get("name") for t in tags2]
    if with_releases and entry.get("status") == "OK":
        st3, rels = gh_json(f"https://api.github.com/repos/{owner_repo}/releases?per_page=100")
        if st3 == 200 and rels is not None:
            entry["releases"] = [{
                "tag": r.get("tag_name"), "name": r.get("name"),
                "url": r.get("html_url"), "created_at": r.get("created_at"),
                "published_at": r.get("published_at"),
                "target_commitish": r.get("target_commitish"),
                "draft": r.get("draft"), "prerelease": r.get("prerelease"),
                "assets": [{
                    "name": a.get("name"), "url": a.get("browser_download_url"),
                    "size": a.get("size"), "content_type": a.get("content_type"),
                    "updated_at": a.get("updated_at"), "downloads": a.get("download_count"),
                } for a in (r.get("assets") or [])],
            } for r in rels]
        else:
            entry["releases"] = None
            results["failures"].append({"url": f"repos/{owner_repo}/releases", "http_status": st3})
    results["repositories"][owner_repo] = entry
    return entry

log_query("github-api", "GET /repos/red/red", "ATTEMPT")
collect_repo("red/red", with_tags=True, with_releases=True)
log_query("github-api", "GET /repos/red/red/tags", "ATTEMPT")
log_query("github-api", "GET /repos/red/red/releases", "ATTEMPT")

log_query("github-api", "GET /orgs/red/repos?per_page=100", "ATTEMPT")
st, org = gh_json("https://api.github.com/orgs/red/repos?per_page=100")
if st == 200 and org:
    results["red_org_repos"] = sorted([r.get("full_name") for r in org])
else:
    results["red_org_repos"] = None
    results["failures"].append({"url": "orgs/red/repos", "http_status": st})

log_query("github-api", "GET /repos/metaeducation/ren-c", "ATTEMPT")
collect_repo("metaeducation/ren-c", with_tags=True, with_releases=True)

log_query("github-api", "GET /repos/rebol/rebol", "ATTEMPT")
collect_repo("rebol/rebol")   # expected historical official R3 repo — may be gone

log_query("github-api", "GET /orgs/rebol/repos", "ATTEMPT")
st, org = gh_json("https://api.github.com/orgs/rebol/repos?per_page=100")
results["rebol_org"] = sorted([r.get("full_name") for r in org]) if st == 200 and org else None
if st != 200:
    results["failures"].append({"url": "orgs/rebol/repos", "http_status": st})

log_query("github-api", "GET /repos/Oldes/Rebol-legacy", "ATTEMPT")
collect_repo("Oldes/Rebol-legacy", with_tags=True, with_releases=True)
log_query("github-api", "GET /repos/Oldes/Rebol3", "ATTEMPT")
collect_repo("Oldes/Rebol3")

# ---- GitHub search API (search rate limit applies; keep small) ----
for q in ["rebol 2.7.8", "red language compiler", "red-system"]:
    log_query("github-search", f"search/repositories q={q!r}", "ATTEMPT")
    st, sr = gh_json(f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&per_page=10")
    if st == 200 and sr:
        results["searches"][q] = [{"full_name": i.get("full_name"),
                                   "url": i.get("html_url"),
                                   "stars": i.get("stargazers_count"),
                                   "description": (i.get("description") or "")[:160]}
                                  for i in sr.get("items", [])]
    else:
        results["searches"][q] = None
        results["failures"].append({"url": f"search/repositories q={q!r}", "http_status": st})
    time.sleep(2)  # be polite to the search rate limit

with open(os.path.join(MAN, "github-discovery.json"), "w") as f:
    json.dump(results, f, indent=2)

print("=== discovery summary ===")
for k, v in results["repositories"].items():
    print(f"{k}: status={v['status']} default_branch={v.get('default_branch')} "
          f"license={v.get('license')} stars={v.get('stars')} tags={len(v['tags']) if v.get('tags') else 'n/a'} "
          f"releases={len(v['releases']) if v.get('releases') else 'n/a'}")
print("red org repos:", results.get("red_org_repos"))
print("rebol org:", results.get("rebol_org"))
print("failures:", json.dumps(results["failures"]))
