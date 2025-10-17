import unittest
from node_helpers import text_node_to_html_node
from textnode import TextNode, TextType
from leafnode import LeafNode


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_type_text(self):
        node = TextNode("Hello world", TextType.TEXT)
        result = text_node_to_html_node(node)
        expected = LeafNode(None, "Hello world")
        self.assertEqual(result, expected)

    def test_text_type_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        result = text_node_to_html_node(node)
        expected = LeafNode("b", "Bold text")
        self.assertEqual(result, expected)

    def test_text_type_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        result = text_node_to_html_node(node)
        expected = LeafNode("i", "Italic text")
        self.assertEqual(result, expected)

    def test_text_type_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        result = text_node_to_html_node(node)
        expected = LeafNode("code", "print('hi')")
        self.assertEqual(result, expected)

    def test_text_type_link(self):
        node = TextNode("Example", TextType.LINK, "https://example.com")
        result = text_node_to_html_node(node)
        expected = LeafNode("a", "Example", {"href": "https://example.com"})
        self.assertEqual(result, expected)

    def test_text_type_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        result = text_node_to_html_node(node)
        expected = LeafNode("img", "", {"src": "https://example.com/image.png", "alt": "Alt text"})
        self.assertEqual(result, expected)

    def test_to_html_output_text(self):
        node = TextNode("Hello", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Hello")

    def test_to_html_output_bold(self):
        node = TextNode("Bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold</b>")

    def test_to_html_output_link(self):
        node = TextNode("Click", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click</a>')

    def test_to_html_output_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/img.png" alt="Alt text">',
        )

    def test_invalid_text_type_raises(self):
        # Make a fake TextNode-like object to simulate an invalid enum
        class FakeTextNode:
            def __init__(self):
                self.text_type = "INVALID"
                self.text = "Something"
                self.url = None

        with self.assertRaises(ValueError):
            text_node_to_html_node(FakeTextNode())


if __name__ == "__main__":
    unittest.main()
