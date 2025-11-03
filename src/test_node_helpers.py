import unittest
import textwrap
from node_helpers import text_node_to_html_node
from node_helpers import split_nodes_delimiter
from node_helpers import extract_markdown_images
from node_helpers import extract_markdown_links
from node_helpers import split_nodes_image
from node_helpers import split_nodes_link
from node_helpers import text_to_textnodes
from node_helpers import markdown_to_blocks
from node_helpers import block_to_block_type
from node_helpers import markdown_to_html_node
from textnode import TextNode, TextType
from leafnode import LeafNode
from blocktype import BlockType


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

class TestMarkdownExtraction(unittest.TestCase):
    def test_single_image(self):
        text = "Here is an image ![alt text](https://example.com/img.png)"
        result = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/img.png")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        text = "Images: ![one](url1) and ![two](url2)"
        result = extract_markdown_images(text)
        expected = [("one", "url1"), ("two", "url2")]
        self.assertEqual(result, expected)

    def test_no_images(self):
        text = "No images here."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

    def test_image_with_special_chars(self):
        text = "Check this ![alt-text](https://example.com/path/to-image.png)"
        result = extract_markdown_images(text)
        expected = [("alt-text", "https://example.com/path/to-image.png")]
        self.assertEqual(result, expected)

    def test_single_link(self):
        text = "Click [here](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("here", "https://example.com")]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        text = "Links: [one](url1) and [two](url2)"
        result = extract_markdown_links(text)
        expected = [("one", "url1"), ("two", "url2")]
        self.assertEqual(result, expected)

    def test_no_links(self):
        text = "No links in this text."
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

    def test_links_ignore_images(self):
        text = "An image ![img](url1) and a link [link](url2)"
        result = extract_markdown_links(text)
        expected = [("link", "url2")]
        self.assertEqual(result, expected)

    def test_link_with_special_chars(self):
        text = "Check [my-link](https://example.com/path?query=1&test=2)"
        result = extract_markdown_links(text)
        expected = [("my-link", "https://example.com/path?query=1&test=2")]
        self.assertEqual(result, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        nodes = [TextNode("Hello ![alt](url.png) world", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1], TextNode("alt", TextType.IMAGE, "url.png"))

    def test_multiple_images(self):
        nodes = [TextNode("![a](1.png) middle ![b](2.png)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "a")
        self.assertEqual(result[0].url, "1.png")
        self.assertEqual(result[1].text, " middle ")
        self.assertEqual(result[2].text, "b")
        self.assertEqual(result[2].url, "2.png")

    def test_adjacent_images(self):
        nodes = [TextNode("![x](1.png)![y](2.png)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "x")
        self.assertEqual(result[0].url, "1.png")
        self.assertEqual(result[1].text, "y")
        self.assertEqual(result[1].url, "2.png")

    def test_no_images(self):
        nodes = [TextNode("Just text", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(result[0].text, "Just text")
    
    def test_ignores_non_text_nodes(self):
        nodes = [TextNode("![alt](url.png)", TextType.IMAGE)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)



class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        nodes = [TextNode("Click [here](https://example.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].text, "here")
        self.assertEqual(result[1].url, "https://example.com")

    def test_multiple_links(self):
        nodes = [TextNode("[a](1.com) middle [b](2.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "a")
        self.assertEqual(result[0].url, "1.com")
        self.assertEqual(result[1].text, " middle ")
        self.assertEqual(result[2].text, "b")
        self.assertEqual(result[2].url, "2.com")

    def test_adjacent_links(self):
        nodes = [TextNode("[x](1.com)[y](2.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "x")
        self.assertEqual(result[0].url, "1.com")
        self.assertEqual(result[1].text, "y")
        self.assertEqual(result[1].url, "2.com")

    def test_no_links(self):
        nodes = [TextNode("Just text", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(result[0].text, "Just text")

    def test_ignores_non_text_nodes(self):
        nodes = [TextNode("[a](1.com)", TextType.LINK, "1.com")]
        result = split_nodes_link(nodes)
        self.assertEqual(result, nodes)

class TestTextToTextNodes(unittest.TestCase):
    def test_sample_line(self):
        sample_text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        result = text_to_textnodes(sample_text)

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(len(result), len(expected_nodes))

        for r_node, e_node in zip(result, expected_nodes):
            self.assertEqual(r_node.text_type, e_node.text_type)
            self.assertEqual(r_node.text, e_node.text)
            self.assertEqual(r_node.url, getattr(e_node, "url", None))

class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        text = "This is a single paragraph."
        expected = ["This is a single paragraph."]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_multiple_blocks(self):
        text = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
        expected = ["Paragraph one.", "Paragraph two.", "Paragraph three."]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_blocks_with_extra_whitespace(self):
        text = "  First block.  \n\n   Second block.\n\nThird block.   "
        expected = ["First block.", "Second block.", "Third block."]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_leading_and_trailing_newlines(self):
        text = "\n\n# Heading\n\nSome text.\n\n"
        expected = ["# Heading", "Some text."]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_empty_string(self):
        text = ""
        expected = []
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_multiple_blank_blocks(self):
        text = "Block one.\n\n\n\nBlock two."
        expected = ["Block one.", "Block two."]
        self.assertEqual(markdown_to_blocks(text), expected)

class TestBlockToBlockType(unittest.TestCase):

    def test_heading_block(self):
        text = "# This is a heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_multilevel_heading(self):
        text = "###### Level 6 heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_code_block(self):
        text = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_inline_code_not_block(self):
        # Should count as paragraph, not code block
        text = "This is a paragraph with `inline code`."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_blockquote(self):
        text = "> This is a quote\n> Continued quote line"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_unordered_list_dash(self):
        text = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(text), BlockType.UL)

    def test_ordered_list(self):
        text = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(text), BlockType.OL)

    def test_malformed_ordered_list(self):
        text = "1. First\n3. Second"
        # Should not count as ordered list (numbers out of sequence)
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_paragraph(self):
        text = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_mixed_list_and_paragraph(self):
        text = "- List item\n\nSome text after list"
        # Not a single block; if passed as one string, treat as paragraph
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_empty_block(self):
        text = ""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = textwrap.dedent("""
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

class TestMarkdownToHTML_Extra(unittest.TestCase):
    def test_mixed_inline_formatting(self):
        md = "This is **bold** and _italic_ plus `code`"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><p>This is <b>bold</b> and <i>italic</i> plus <code>code</code></p></div>"
        self.assertEqual(html, expected)

    def test_paragraphs_with_blank_lines(self):
        md = "First paragraph.\n\nSecond paragraph.\n\n\nThird paragraph."
        html = markdown_to_html_node(md).to_html()
        expected = "<div><p>First paragraph.</p><p>Second paragraph.</p><p>Third paragraph.</p></div>"
        self.assertEqual(html, expected)

    def test_codeblock_with_indentation(self):
        md = "```\ndef func():\n    return 42\n```"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><pre><code>def func():\n    return 42\n</code></pre></div>"
        self.assertEqual(html, expected)

    def test_inline_code_with_backticks(self):
        md = "Use `code` in text"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><p>Use <code>code</code> in text</p></div>"
        self.assertEqual(html, expected)

    def test_paragraph_then_codeblock(self):
        md = "Intro text:\n\n```\nline 1\nline 2\n```"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><p>Intro text:</p><pre><code>line 1\nline 2\n</code></pre></div>"
        self.assertEqual(html, expected)

    def test_unordered_list_basic(self):
        md = "- Item one\n- Item two\n- Item three"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>"
        self.assertEqual(html, expected)

    def test_ordered_list_basic(self):
        md = "1. First\n2. Second\n3. Third"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>"
        self.assertEqual(html, expected)

    def test_blockquote_basic(self):
        md = "> A wise quote\n> continues here"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><blockquote>A wise quote continues here</blockquote></div>"
        self.assertEqual(html, expected)

    def test_heading_basic(self):
        md = "## Subheading Level 2"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><h2>Subheading Level 2</h2></div>"
        self.assertEqual(html, expected)

    def test_empty_input_raises_for_parentnode(self):
        md = ""
        with self.assertRaises(ValueError):
            markdown_to_html_node(md).to_html()

if __name__ == "__main__":
    unittest.main()