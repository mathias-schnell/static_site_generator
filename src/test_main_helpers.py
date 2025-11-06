import unittest
from main_helpers import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_single_h1_header(self):
        markdown = "# My Title"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_h1_with_extra_spaces(self):
        markdown = "#   My Title   "
        self.assertEqual(extract_title(markdown), "My Title")

    def test_h1_not_on_first_line(self):
        markdown = "Intro text\n# Page Title\nMore text"
        self.assertEqual(extract_title(markdown), "Page Title")

    def test_multiple_headers_returns_first(self):
        markdown = "# First Title\n## Subtitle\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_no_h1_header_raises_exception(self):
        markdown = "## Subtitle\n### Smaller Header"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_text_with_hash_not_header(self):
        markdown = "This line has a # but isn’t a header"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_header_with_inline_hash(self):
        markdown = "# Title with # symbol inside"
        self.assertEqual(extract_title(markdown), "Title with # symbol inside")

if __name__ == "__main__":
    unittest.main()