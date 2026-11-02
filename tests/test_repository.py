from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "SKILL.md", "LICENSE",
    "references/workspace-init.md", "references/branch-init.md",
    "references/maintenance.md", "references/handoff.md",
    "references/deployment.md", "templates/workspace-config.yaml",
    "templates/branch-readme.md", ".github/workflows/validate.yml",
]

def read_product(test_case, path):
    test_case.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
    return path.read_text()

class RepositoryTests(unittest.TestCase):
    def test_required_files_exist(self):
        for rel in REQUIRED:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_frontmatter_contract(self):
        text = read_product(self, ROOT / "SKILL.md")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1].strip().splitlines()
        keys = [line.split(":", 1)[0] for line in frontmatter]
        self.assertEqual(keys, ["name", "description"])
        self.assertEqual(frontmatter[0], "name: agent-multi-repo-worktree-dev")
        self.assertIn("description: Use when ", frontmatter[1])

    def test_relative_markdown_links_resolve(self):
        files = [ROOT / "README.md", ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
        for file in files:
            text = read_product(self, file)
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                path = target.split("#", 1)[0]
                self.assertTrue((file.parent / path).exists(), f"{file}: {target}")

    def test_no_personal_or_placeholder_content(self):
        files = [ROOT / "README.md", ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
        excluded = "d" + "p"
        for file in files:
            text = read_product(self, file)
            self.assertNotRegex(text, r"(?i)\b" + excluded + r"\b")
            self.assertNotIn("/" + "Users" + "/", text)
            for marker in ("T" + "BD", "T" + "ODO"):
                self.assertNotRegex(text, r"\b" + marker + r"\b")

if __name__ == "__main__":
    unittest.main()
