from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER_ENTRY = re.compile(r"file\s*:\s*['\"]([^'\"]+)['\"]")
REMOTE_RESOURCE = re.compile(
    r"(?is)(?:"
    r"<(?:script|img|iframe|audio|video|source|link)\b[^>]*(?:src|href)\s*=\s*['\"]https?://"
    r"|url\(\s*['\"]?https?://"
    r"|fetch\(\s*['\"]https?://"
    r"|new\s+WebSocket\(\s*['\"]wss?://"
    r")"
)


class StaticSiteSmokeTest(unittest.TestCase):
    def test_launcher_references_existing_game_files(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        game_paths = LAUNCHER_ENTRY.findall(index)

        self.assertGreater(len(game_paths), 0, "The launcher should expose at least one game")
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
                self.assertRegex(document, r'(?is)<html\s+[^>]*lang=["\']ru["\']')
                self.assertRegex(document, r'(?is)<meta\s+charset=["\']utf-8["\']')
                self.assertRegex(document, r"(?is)<title>\s*[^<]+\s*</title>")
                self.assertRegex(document, r'(?is)<meta\s+name=["\']viewport["\']')

    def test_html_entries_do_not_load_remote_resources(self):
        html_paths = [ROOT / "index.html", *(ROOT / "game").glob("*.html")]

        for path in html_paths:
            with self.subTest(path=path.relative_to(ROOT)):
                document = path.read_text(encoding="utf-8")
                self.assertIsNone(
                    REMOTE_RESOURCE.search(document),
                    f"Remote resource loading found in {path.relative_to(ROOT)}",
                )

    def test_launcher_has_small_screen_layout(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn("@media (max-width:700px)", index)
        self.assertRegex(index, r"\.layout\s*\{grid-template-columns:1fr\}")
        self.assertRegex(index, r"\.frameWrap\s*\{height:70vh;min-height:480px\}")
        self.assertIn("@media (max-width:420px)", index)


if __name__ == "__main__":
    unittest.main()
