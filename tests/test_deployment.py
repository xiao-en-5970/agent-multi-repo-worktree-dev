from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read_product(test_case, relative):
    path = ROOT / relative
    test_case.assertTrue(path.is_file(), f"missing {relative}")
    return path.read_text()

class DeploymentTests(unittest.TestCase):
    def test_deployment_requires_per_repository_static_evidence(self):
        text = read_product(self, "references/deployment.md")
        for token in [
            "每个目标仓库", ".gitlab-ci.yml", ".github/workflows/",
            "Jenkinsfile", "include", "目标 commit", "不 source",
            "不执行部署脚本", "expressions", "可变 ref", "行号",
            "不默认", "单独确认",
        ]:
            self.assertIn(token, text)

if __name__ == "__main__":
    unittest.main()
