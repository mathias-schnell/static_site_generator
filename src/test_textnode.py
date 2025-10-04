import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_different_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_different_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_eq_different_url(self):
        node1 = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://other.com")
        self.assertNotEqual(node1, node2)

    def test_eq_url_none_and_value(self):
        node1 = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK, "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_not_eq_non_textnode(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "Not a TextNode")

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        expected = "TextNode(This is a text node, TextType.BOLD, https://example.com)"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
