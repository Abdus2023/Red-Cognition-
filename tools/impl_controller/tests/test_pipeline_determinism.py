"""Pipeline-level determinism + gap analysis tests.

Verifies the full 5-stage pipeline produces deterministic output and surfaces
the requirement-to-task coverage gap honestly.
Run via:  python3 tools/impl-controller.py --self-test
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent.parent
REPO_ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))


def _run_pipeline(status_out):
    r = subprocess.run(
        [sys.executable, str(TOOLS / "run-full-pipeline.py")],
        capture_output=True, text=True, timeout=60)
    return r


def _norm(status):
    """Normalize pipeline output (exclude timestamps/head)."""
    return json.dumps({k: v for k, v in status.items()
                       if k not in ("started_at", "completed_at", "repository_head")},
                      sort_keys=True)


# ==========================================================================
class PipelineDeterminism(unittest.TestCase):
    def test_pipeline_deterministic(self):
        """Three pipeline runs produce identical normalized output."""
        norms = []
        for _ in range(3):
            r = _run_pipeline(None)
            self.assertEqual(r.returncode, 0, r.stderr[:200])
            status_path = REPO_ROOT / "docs" / "implementation" / "full-pipeline-status.json"
            status = json.loads(status_path.read_text())
            norms.append(_norm(status))
        self.assertEqual(len(set(norms)), 1)

    def test_pipeline_frontier_unchanged(self):
        """Pipeline always reports READY=0 / BLOCKED=4 / PAUSED."""
        r = _run_pipeline(None)
        self.assertEqual(r.returncode, 0)
        status = json.loads(
            (REPO_ROOT / "docs" / "implementation" / "full-pipeline-status.json").read_text())
        s5 = status["stage5_control"]
        self.assertEqual(s5["frontier"], "PAUSED")
        self.assertEqual(s5["graph"]["READY"], 0)
        self.assertEqual(s5["graph"]["BLOCKED"], 4)


# ==========================================================================
class CoverageGapAnalysis(unittest.TestCase):
    def test_coverage_gap_surfaced(self):
        """Pipeline surfaces 0% structured coverage honestly."""
        r = _run_pipeline(None)
        status = json.loads(
            (REPO_ROOT / "docs" / "implementation" / "full-pipeline-status.json").read_text())
        cov = status.get("stage3_traceability", {}).get("coverage", {})
        # 0% coverage is the HONEST result — tasks use informal refs
        self.assertEqual(cov.get("requirements_with_tasks"), 0)
        self.assertGreater(cov.get("total_structured_requirements", 0), 1000)

    def test_epistemic_gap_explicit(self):
        """specified > implemented > executed."""
        status = json.loads(
            (REPO_ROOT / "docs" / "implementation" / "full-pipeline-status.json").read_text())
        eps = status["epistemic_states"]
        self.assertGreater(eps["specified"], eps["implemented"])
        self.assertGreater(eps["implemented"], eps["executed"])
        self.assertEqual(eps["tested"], 0)
        self.assertEqual(eps["validated"], 0)
        self.assertEqual(eps["evidenced"], 0)
        self.assertEqual(eps["formally_verified"], 0)

    def test_requirements_inventory_consistent(self):
        """Requirements inventory file exists and has > 1000 entries."""
        inv_path = REPO_ROOT / "docs" / "implementation" / "requirements-inventory.json"
        if not inv_path.exists():
            self.skipTest("run stage1 first")
        inv = json.loads(inv_path.read_text())
        self.assertGreater(inv["total"], 1000)
        self.assertGreater(inv["by_strength"]["mandatory"], 500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
