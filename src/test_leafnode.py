import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_defaults(self):
        """Test LeafNode with all default parameters."""
        node = LeafNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.props, {})

    def test_custom_values(self):
        """Test LeafNode with custom tag, value, and props."""
        props = {"class": "greeting", "id": "first"}
        node = LeafNode(tag="p", value="Hello", props=props)

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, props)

    def test_eq_same(self):
        """Test equality of two identical LeafNode instances."""
        node1 = LeafNode("p", "Hello", {"class": "greeting"})
        node2 = LeafNode("p", "Hello", {"class": "greeting"})
        self.assertEqual(node1, node2)

    def test_eq_different(self):
        """Test inequality when one attribute differs."""
        node1 = LeafNode("p", "Hello", {"class": "greeting"})
        node2 = LeafNode("p", "Hello", {"class": "farewell"})
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        """Test __repr__ outputs the expected multi-line string."""
        node = LeafNode("p", "Hello", {"class": "greeting"})
        expected = (
            "LeafNode(\n"
            "  tag='p',\n"
            "  value='Hello',\n"
            "  props={'class': 'greeting'}\n"
            ")"
        )
        self.assertEqual(repr(node), expected)

    def test_to_html_with_tag_and_props(self):
        """Test HTML output with a tag and props."""
        node = LeafNode("p", "Hello", {"class": "greeting"})
        self.assertEqual(node.to_html(), '<p class="greeting">Hello</p>')

    def test_to_html_with_tag_no_props(self):
        """Test HTML output with a tag but no props."""
        node = LeafNode("p", "Hello")
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_to_html_no_tag(self):
        """If tag is None, to_html should return only the value."""
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_no_value_raises(self):
        """If value is None, to_html should raise ValueError."""
        node = LeafNode("p")
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
