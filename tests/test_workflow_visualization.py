from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs/visualizations/standard-workflow.html"


class WorkflowPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.svg_count = 0
        self.animate_count = 0
        self.section_ids = set()
        self.button_ids = set()
        self.external_references = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "svg":
            self.svg_count += 1
        if tag in {"animate", "animateTransform", "animateMotion"}:
            self.animate_count += 1
        if tag == "section" and "id" in values:
            self.section_ids.add(values["id"])
        if tag == "button" and "id" in values:
            self.button_ids.add(values["id"])
        for name in ("src", "href", "xlink:href"):
            value = values.get(name, "")
            if value.startswith(("https://", "http://", "//")):
                self.external_references.append(value)


class WorkflowVisualizationTests(unittest.TestCase):
    def read_page(self):
        self.assertTrue(PAGE.is_file(), "missing docs/visualizations/standard-workflow.html")
        text = PAGE.read_text()
        self.parser = WorkflowPageParser()
        self.parser.feed(text)
        return text

    def test_page_has_six_narrative_scenes_and_svg_animation(self):
        parser_text = self.read_page()
        expected = {
            "boundary", "preflight", "isolation",
            "evidence", "handoff", "advantages",
        }
        self.assertEqual(self.parser.section_ids, expected)
        self.assertGreaterEqual(self.parser.svg_count, 6)
        self.assertGreaterEqual(self.parser.animate_count, 8)
        self.assertIn("规范不是额外负担", parser_text)

    def test_page_is_offline_accessible_and_motion_controllable(self):
        self.read_page()
        self.assertEqual(self.parser.external_references, [])
        self.assertIn("motion-toggle", self.parser.button_ids)
        self.assertIn("prefers-reduced-motion", PAGE.read_text())


if __name__ == "__main__":
    unittest.main()
