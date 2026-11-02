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

    def test_metadata_targets_are_contained_and_rechecked_before_every_write(self):
        text = read_product(self, "references/workspace-init.md")
        for token in [
            "`.branch-worktree/` 和 `config.yaml`",
            "最近现有祖先",
            "解析后的物理路径必须位于工作区内",
            "符号链接或文件类型碰撞",
            "每次创建或更新前重新解析并复核",
        ]:
            self.assertIn(token, text)

        scenario = read_product(self, "tests/scenarios/config-path-safety.md")
        self.assertIn(
            "stop at `<workspace>/.branch-worktree/config.yaml` before every write; "
            "do not create, modify, or delete the metadata directory, configuration, "
            "base directories, repositories, or external symlink target.",
            scenario,
        )

    def test_root_level_worktree_layout_is_explicitly_supported(self):
        text = read_product(self, "references/workspace-init.md")
        for token in [
            "根级布局", "worktreeDir: .", "并列", "显式选择",
            "已登记仓库", "不得为绝对路径",
        ]:
            self.assertIn(token, text)
        template = read_product(self, "templates/workspace-config.yaml")
        self.assertIn("# worktreeDir: .", template)
        skill = read_product(self, "SKILL.md")
        self.assertIn("root-level layout", skill)
        self.assertIn("branch paths must avoid `mainDir`", skill)

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
