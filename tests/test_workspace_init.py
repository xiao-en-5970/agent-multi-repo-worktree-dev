from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read_product(test_case, relative):
    path = ROOT / relative
    test_case.assertTrue(path.is_file(), f"missing {relative}")
    return path.read_text()

class WorkspaceInitTests(unittest.TestCase):
    def test_reference_defines_first_use_gate_and_safety(self):
        text = read_product(self, "references/workspace-init.md")
        for token in [
            "main", "WorkTree", "共同父目录", "不递归扫描",
            "rev-parse --show-toplevel", "重复键", "最近现有祖先",
            "部分完成", "待登记仓库", "基线漂移",
        ]:
            self.assertIn(token, text)

    def test_template_has_exact_version_one_fields(self):
        text = read_product(self, "templates/workspace-config.yaml")
        for token in [
            "version: 1", "mainDir: main", "worktreeDir: WorkTree",
            "repositories:", "name: example-api", "path: api",
            "url: git@example.com:team/example-api.git",
            "remote: origin", "defaultBranch: main",
        ]:
            self.assertIn(token, text)
        self.assertNotIn("profile:", text)

if __name__ == "__main__":
    unittest.main()
