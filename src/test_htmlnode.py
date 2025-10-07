import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_custom_values(self):
        children = ["child1", "child2"]
        props = {"class": "container", "id": "main"}
        node = HTMLNode(tag="div", value="Hello", children=children, props=props)

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"style": "color:red"})
        expected = (
            "HTMLNode(\n"
            "  tag='p',\n"
            "  value='Hello',\n"
            "  children=[],\n"
            "  props={'style': 'color:red'}\n"
            ")"
        )
        self.assertEqual(repr(node), expected)

    def test_to_html_raises(self):
        node = HTMLNode("p", "text")
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
