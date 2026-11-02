from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read_product(test_case, relative):
    path = ROOT / relative
    test_case.assertTrue(path.is_file(), f"missing {relative}")
    return path.read_text()

class BranchHandoffTests(unittest.TestCase):
    def test_branch_rules_cover_collisions_remotes_and_existing_branches(self):
        text = read_product(self, "references/branch-init.md")
        for token in [
            "git check-ref-format --branch", "branchDir", "最近现有祖先",
            "fetch", "完整 SHA", "基线漂移", "不 reset", "不 rebase",
            "本地分支", "所选 remote", "父级或子级", "tmp",
        ]:
            self.assertIn(token, text)
        self.assertIn(
            "分支已在其他 worktree 检出：报冲突并停止分支初始化，禁止后续任何写入",
            text,
        )

    def test_handoff_and_template_share_status_contract(self):
        reference = read_product(self, "references/handoff.md")
        template = read_product(self, "templates/branch-readme.md")
        for status in ["未开始", "进行中", "阻塞", "完成", "不适用"]:
            self.assertIn(status, reference)
            self.assertIn(status, template)
        for token in ["基线", "当前 commit", "验证证据", "负责人", "下一步"]:
            self.assertIn(token, template)

if __name__ == "__main__":
    unittest.main()
