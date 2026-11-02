from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read_product(test_case, relative):
    path = ROOT / relative
    test_case.assertTrue(path.is_file(), f"missing {relative}")
    return path.read_text()

class MaintenanceTests(unittest.TestCase):
    def test_maintenance_preserves_work_and_evidence(self):
        text = read_product(self, "references/maintenance.md")
        for token in [
            "git worktree list --porcelain", "git status --short --branch",
            "git worktree repair", "git worktree prune", "locked",
            "未推送", "默认保留", "归档校验", "--force", "reset --hard",
        ]:
            self.assertIn(token, text)

if __name__ == "__main__":
    unittest.main()
