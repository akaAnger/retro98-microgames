from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER_ENTRY = re.compile(r"file\s*:\s*['\"]([^'\"]+)['\"]")


class StaticSiteSmokeTest(unittest.TestCase):
    def test_launcher_references_existing_game_files(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        game_paths = LAUNCHER_ENTRY.findall(index)

        self.assertEqual(len(game_paths), 5, "The launcher should expose five games")
        self.assertEqual(len(game_paths), len(set(game_paths)), "Launcher paths must be unique")

        for relative_path in game_paths:
            with self.subTest(path=relative_path):
                path = ROOT / relative_path
                self.assertTrue(path.is_file(), f"Launcher target does not exist: {relative_path}")

    def test_launcher_exposes_every_game_html_file(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        launcher_paths = set(LAUNCHER_ENTRY.findall(index))
        game_files = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "game").glob("*.html")
        }

        self.assertSetEqual(
            launcher_paths,
            game_files,
            "Every game HTML file should be reachable from the launcher and no launcher entry should point outside game/",
        )

    def test_all_html_entries_have_basic_document_metadata(self):
        html_paths = [ROOT / "index.html", *(ROOT / "game").glob("*.html")]

        self.assertGreater(len(html_paths), 1, "No game HTML files were found")

        for path in html_paths:
            with self.subTest(path=path.relative_to(ROOT)):
                document = path.read_text(encoding="utf-8")
                self.assertRegex(document, r"(?i)^\s*<!doctype\s+html>")
                self.assertRegex(document, r"(?is)<title>\s*[^<]+\s*</title>")
                self.assertRegex(document, r'(?is)<meta\s+name=["\']viewport["\']')


if __name__ == "__main__":
    unittest.main()
