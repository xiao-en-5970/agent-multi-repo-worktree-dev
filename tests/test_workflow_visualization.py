from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs/visualizations/standard-workflow.html"
INDEX = ROOT / "docs/index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section_ids = set()
        self.external_references = []
        self.animate_count = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "section" and "id" in values:
            self.section_ids.add(values["id"])
        if tag in {"animate", "animateTransform", "animateMotion"}:
            self.animate_count += 1
        for name in ("src", "href", "xlink:href"):
            value = values.get(name, "")
            if value.startswith(("https://", "http://", "//")):
                self.external_references.append(value)


class WorkflowVisualizationTests(unittest.TestCase):
    def read_page(self):
        self.assertTrue(PAGE.is_file(), "missing docs/visualizations/standard-workflow.html")
        text = PAGE.read_text()
        parser = PageParser()
        parser.feed(text)
        return text, parser

    def test_page_explains_main_worktree_and_tmp(self):
        text, parser = self.read_page()
        self.assertEqual(parser.section_ids, {"directories", "tmp", "readme", "value"})
        for phrase in [
            "main/", "WorkTree/", "tmp/",
            "本次需求的产物", "tmp/README.md", "把每个改动放大",
        ]:
            self.assertIn(phrase, text)

    def test_readme_contract_matches_handoff_template(self):
        text, _ = self.read_page()
        for heading in ["# 阻塞项", "# 当前摘要", "# 目标", "# 共用分支", "# 仓库矩阵",
                        "# 验证证据", "# 下一步", "# 关键决策", "# 变更日志"]:
            self.assertIn(heading, text)
        for field in ["基线 commit（完整 SHA）", "当前 commit（完整 SHA）", "执行目录",
                      "未开始", "进行中", "阻塞", "完成", "不适用"]:
            self.assertIn(field, text)
        for field in ["改了什么", "为什么改", "影响范围", "改动前", "改动后", "风险 / 回滚"]:
            self.assertIn(field, text)

    def test_tmp_boundary_and_cleanup_gate_are_explicit(self):
        text, _ = self.read_page()
        for phrase in ["各仓库 worktree 之外", "不被任何仓库 Git 跟踪",
                       "不是 IDE 或构建临时目录", "默认保留",
                       "单独确认归档目的地", "归档校验"]:
            self.assertIn(phrase, text)

    def test_page_is_clean_offline_and_without_motion_overlays(self):
        text, parser = self.read_page()
        self.assertEqual(parser.external_references, [])
        self.assertEqual(parser.animate_count, 0)
        self.assertNotIn("position:fixed", text)
        self.assertNotIn("position: absolute", text)

    def test_docs_root_redirects_to_workflow_page(self):
        self.assertTrue(INDEX.is_file(), "missing docs/index.html")
        index = INDEX.read_text()
        self.assertIn('http-equiv="refresh"', index)
        self.assertIn('content="0; url=visualizations/standard-workflow.html"', index)
        self.assertIn('href="visualizations/standard-workflow.html"', index)
        self.assertTrue((INDEX.parent / "visualizations/standard-workflow.html").is_file())
        parser = PageParser()
        parser.feed(index)
        self.assertEqual(parser.animate_count, 0)
        self.assertNotIn("animation", index.lower())
        self.assertNotIn("@keyframes", index.lower())


if __name__ == "__main__":
    unittest.main()
