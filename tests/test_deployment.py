from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read_product(test_case, relative):
    path = ROOT / relative
    test_case.assertTrue(path.is_file(), f"missing {relative}")
    return path.read_text()

class DeploymentTests(unittest.TestCase):
    def test_merge_direction_is_one_way_to_protect_development_branch(self):
        deployment = read_product(self, "references/deployment.md")
        for token in [
            "单向合并", "只允许开发分支 **into** 部署分支", "禁止反向合并",
            "污染", "部署分支", "开发分支", "git log <deploy>..<dev>",
            "git log <dev>..<deploy>", "停止部署写操作",
            "不自动 reset、rebase、force-push",
            "禁止把部署分支合并回开发分支",
        ]:
            self.assertIn(token, deployment)

        branch = read_product(self, "references/branch-init.md")
        for token in [
            "选定的开发分支不得已被目标部署分支污染",
            "禁止把部署分支反向合入开发分支",
            "只允许 **into** 目标部署分支",
            "部署分支不得合回开发分支",
            "不得作为开发分支的同步来源",
        ]:
            self.assertIn(token, branch)

        skill = read_product(self, "SKILL.md")
        for token in ["one-way", "must not pollute", "never merge", "reverse-merging"]:
            self.assertIn(token, skill)

        readme = read_product(self, "README.md")
        for token in [
            "Merge Direction and Deployment Isolation", "one-way",
            "must not pollute the development branch", "reverse-merging",
        ]:
            self.assertIn(token, readme)

        scenario = read_product(self, "tests/scenarios/deployment-direction.md")
        for token in [
            "Keep merge direction one-way",
            "only the development branch merges into the deployment branch",
            "Do not merge, rebase, pull, reset, or cherry-pick the deployment branch back into the development branch",
            "Reproduce the hotfix on the development branch",
            "report the pollution and stop deployment writes",
        ]:
            self.assertIn(token, scenario)

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
