import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_defaults(self):
        """Test ParentNode with children and props defaults."""
        # children should not be None; must be a list
        child = LeafNode("p", "Hello")
        node = ParentNode("div", [child])
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {})  # default props

    def test_custom_props_and_children(self):
        """Test ParentNode with custom props and multiple children."""
        children = [LeafNode("p", "Hello"), LeafNode("p", "World")]
        props = {"class": "container", "id": "main"}
        node = ParentNode("div", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_eq_same(self):
        """Test equality of identical ParentNodes."""
        children = [LeafNode("p", "Hello")]
        props = {"class": "test"}
        node1 = ParentNode("div", children, props)
        node2 = ParentNode("div", children, props)
        self.assertEqual(node1, node2)

    def test_eq_different(self):
        """Test inequality with different tag, children, or props."""
        node1 = ParentNode("div", [LeafNode("p", "Hello")])
        node2 = ParentNode("section", [LeafNode("p", "Hello")])
        node3 = ParentNode("div", [LeafNode("p", "World")])
        node4 = ParentNode("div", [LeafNode("p", "Hello")], {"class": "test"})
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)

    def test_repr(self):
        """Test __repr__ outputs the expected multi-line string."""
        children = [LeafNode("p", "Hello")]
        props = {"class": "greeting"}
        node = ParentNode("div", children, props)
        expected = (
            "ParentNode(\n"
            "  tag='div',\n"
            f"  children={children!r},\n"
            "  props={'class': 'greeting'}\n"
            ")"
        )
        self.assertEqual(repr(node), expected)

    def test_to_html_raises_no_tag(self):
        """Test that to_html raises error if tag is None."""
        children = [LeafNode("p", "Hello")]
        node = ParentNode(None, children)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_raises_no_children(self):
        """Test that to_html raises error if children list is empty."""
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_simple(self):
        """Test simple HTML generation with one child."""
        child = LeafNode("p", "Hello")
        node = ParentNode("div", [child])
        expected = "<div><p>Hello</p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_multiple_children(self):
        """Test HTML generation with multiple children."""
        children = [LeafNode("p", "Hello"), LeafNode("p", "World")]
        node = ParentNode("div", children)
        expected = "<div><p>Hello</p><p>World</p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_nested_parentnodes(self):
        """Test recursive HTML generation with nested ParentNodes."""
        leaf1 = LeafNode("span", "A")
        leaf2 = LeafNode("span", "B")
        child_parent = ParentNode("p", [leaf1, leaf2])
        root = ParentNode("div", [child_parent])
        expected = "<div><p><span>A</span><span>B</span></p></div>"
        self.assertEqual(root.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
