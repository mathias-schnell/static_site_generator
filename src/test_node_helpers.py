import unittest
from node_helpers import text_node_to_html_node
from node_helpers import split_nodes_delimiter
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

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_with_backticks_code(self):
        nodes = [TextNode("This is `code` text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_nodes_with_italics(self):
        nodes = [TextNode("This is _italic_ text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)

    def test_split_nodes_with_bold(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_split_nodes_with_multiple_delimiters(self):
        nodes = [TextNode("Some `code` and more `stuff`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[3].text, "stuff")
        self.assertEqual(result[3].text_type, TextType.CODE)

    def test_split_nodes_with_multiple_textnodes(self):
        nodes = [
            TextNode("First _one_", TextType.TEXT),
            TextNode(" and _two_", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[3].text_type, TextType.ITALIC)

    def test_split_nodes_with_unmatched_delimiter_raises_error(self):
        nodes = [TextNode("This is `unmatched text", TextType.TEXT)]
        with self.assertRaisesRegex(Exception, "invalid markdown syntax"):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_split_nodes_with_no_delimiter(self):
        nodes = [TextNode("Just plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_with_adjacent_delimiters(self):
        nodes = [TextNode("`one``two`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "one")
        self.assertEqual(result[0].text_type, TextType.CODE)
        self.assertEqual(result[1].text, "two")
        self.assertEqual(result[1].text_type, TextType.CODE)

if __name__ == "__main__":
    unittest.main()
