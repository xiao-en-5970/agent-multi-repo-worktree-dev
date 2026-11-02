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

    def test_all_branch_sources_and_targets_are_resolved_before_any_write(self):
        text = read_product(self, "references/branch-init.md")
        for token in [
            "在任何 `tmp/`、worktree 或分支写入之前",
            "每个仓库的本地分支和所选 remote 的同名分支",
            "现有目标及占用状态",
            "仅当本地与所选 remote 的 ref 解析为完全相同的完整 SHA 时才去重",
            "分歧、多个来源或目标歧义",
            "全局停止整个初始化",
            "保持既有来源优先级",
        ]:
            self.assertIn(token, text)

        preflight = text.index("在任何 `tmp/`、worktree 或分支写入之前")
        write = text.index("**校验通过后写入。**")
        self.assertLess(preflight, write)

    def test_branch_init_accepts_requirement_and_optional_repository_list(self):
        text = read_product(self, "references/branch-init.md")
        for token in [
            "需求来源", "共用分支名", "可选", "候选仓库", "需求文档",
            "服务名", "接口/页面范围", "不得仅凭名称", "前后端联调",
            "确认候选仓库", "不自动 clone",
        ]:
            self.assertIn(token, text)

    def test_readme_separates_first_use_from_ongoing_requirements(self):
        readme = read_product(self, "README.md")
        for token in [
            "First Use", "Ongoing Use", "Do not create branch worktrees in this step",
            "optional", "infer them from the requirement", "frontend/backend",
            "separately confirmed actions",
        ]:
            self.assertIn(token, readme)
        skill = read_product(self, "SKILL.md")
        for token in [
            "First-use setup requires only the two base directories as initial input",
            "repositories may be named explicitly or derived from the requirement",
            "one initialization pass",
        ]:
            self.assertIn(token, skill)

    def test_handoff_and_template_share_status_contract(self):
        reference = read_product(self, "references/handoff.md")
        template = read_product(self, "templates/branch-readme.md")
        for status in ["未开始", "进行中", "阻塞", "完成", "不适用"]:
            self.assertIn(status, reference)
            self.assertIn(status, template)
        for token in ["基线", "当前 commit", "验证证据", "负责人", "下一步"]:
            self.assertIn(token, template)

    def test_matrix_evidence_cells_require_actual_relative_links(self):
        for relative in ["references/handoff.md", "templates/branch-readme.md"]:
            with self.subTest(document=relative):
                text = read_product(self, relative)
                for token in [
                    "每个“验证证据”单元格",
                    "Markdown 链接",
                    "相对 `tmp/README.md`",
                    "替换",
                    "实际目标",
                    "不得原样复制",
                ]:
                    self.assertIn(token, text)

    def test_missing_evidence_requires_linked_tmp_pending_record(self):
        for relative in ["references/handoff.md", "templates/branch-readme.md"]:
            with self.subTest(document=relative):
                text = read_product(self, relative)
                for token in [
                    "证据缺失",
                    "tmp/",
                    "待补证据记录",
                    "缺失命令",
                    "负责人",
                    "所需结果",
                    "链接到该记录",
                    "不得编造",
                ]:
                    self.assertIn(token, text)

if __name__ == "__main__":
    unittest.main()
