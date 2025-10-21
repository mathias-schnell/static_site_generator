import re
from leafnode import LeafNode
from textnode import TextType
from textnode import TextNode

def text_node_to_html_node(text_node):
    newLeaf = LeafNode(None, text_node.text, {})
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            text = node.text
            text_start = 0

            while True:
                del_start = text.find(delimiter, text_start)
                if del_start == -1:
                    if text_start < len(text):
                        new_nodes.append(TextNode(text[text_start:], TextType.TEXT))
                    break

                if del_start > text_start:
                    new_nodes.append(TextNode(text[text_start:del_start], TextType.TEXT))
                
                del_end = text.find(delimiter, del_start + len(delimiter))
                if del_end == -1:
                    raise ValueError(f"invalid markdown syntax: closing delimiter for |{delimiter}| not found")

                del_text = text[del_start + len(delimiter):del_end]
                new_nodes.append(TextNode(del_text, text_type))
                text_start = del_end + len(delimiter)
        
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)