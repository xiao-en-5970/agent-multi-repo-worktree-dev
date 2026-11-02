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

    def test_readme_contract_has_traceable_change_fields(self):
        text, _ = self.read_page()
        for field in ["改了什么", "为什么改", "影响范围", "改动前", "改动后", "验证", "commit"]:
            self.assertIn(field, text)
        self.assertIn("阻塞", text)
        self.assertIn("下一步", text)

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


if __name__ == "__main__":
    unittest.main()
