import re
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextType
from textnode import TextNode
from blocktype import BlockType

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

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        text_start = 0

        for match in extract_markdown_images(text):
            match_text = f"![{match[0]}]({match[1]})"
            split_start = text.find(match_text, text_start)
            split_end = split_start + len(match_text)

            if split_start == -1:
                if text_start < len(text):
                    new_nodes.append(TextNode(text[text_start:], TextType.TEXT))
                break

            if split_start > text_start:
                new_nodes.append(TextNode(text[text_start:split_start], TextType.TEXT))
            
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            text_start = split_end

        if text_start < len(text):
            new_nodes.append(TextNode(text[text_start:], TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        text_start = 0

        for match in extract_markdown_links(text):
            match_text = f"[{match[0]}]({match[1]})"
            split_start = text.find(match_text, text_start)
            split_end = split_start + len(match_text)

            if split_start == -1:
                if text_start < len(text):
                    new_nodes.append(TextNode(text[text_start:], TextType.TEXT))
                break

            if split_start > text_start:
                new_nodes.append(TextNode(text[text_start:split_start], TextType.TEXT))
            
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            text_start = split_end

        if text_start < len(text):
            new_nodes.append(TextNode(text[text_start:], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(text):
    return [p.strip() for p in text.split("\n\n") if p.strip() != ""]

def is_ordered_list_block(text):
    lines = [line for line in text.split('\n') if line.strip()]
    pattern = re.compile(r'^(\d+)\.\s')

    expected = 1
    for line in lines:
        match = pattern.match(line)
        if not match or int(match.group(1)) != expected:
            return False
        expected += 1
    return True

def block_to_block_type(text):
    if not text.strip():
        return BlockType.PARAGRAPH
    
    lines = text.split("\n")
    match_heading = r"^[#]{1,6}\s\S"

    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    elif re.match(match_heading, text):
        return BlockType.HEADING
    elif all(line.startswith('>') for line in lines if line.strip()):
        return BlockType.QUOTE
    elif all(line.startswith('- ') for line in lines if line.strip()):
        return BlockType.UL
    elif is_ordered_list_block(text):
        return BlockType.OL
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(text):
    rootnode = ParentNode("div", None)
    blocks = markdown_to_blocks(text)

    for block in blocks:
        blocktype = block_to_block_type(block)
        child_nodes = tag = ""

        match blocktype:
            case BlockType.CODE:
                tag = "pre"
                child_nodes = [LeafNode("code", block[3:-3].lstrip("\n"))]
            case BlockType.QUOTE:
                tag = "blockquote"
                block = " ".join(line.lstrip("> ").rstrip() for line in block.split("\n"))
                child_nodes = [text_node_to_html_node(n) for n in text_to_textnodes(block)]
            case BlockType.HEADING:
                tag = "h" + str(len(re.match(r"^#+", block).group()))
                child_nodes = [text_node_to_html_node(n) for n in text_to_textnodes(block[block.find(" ") + 1:])]
            case BlockType.UL:
                tag = "ul"
                lines = (line[2:] if line.startswith("- ") else line for line in block.split("\n"))
                child_nodes = [
                    ParentNode("li", [text_node_to_html_node(n) for n in text_to_textnodes(item)])
                    for item in lines
                ]
            case BlockType.OL:
                tag = "ol"
                lines = (line[line.find(" ") + 1:] if re.match(r'^(\d+)\.\s', line) else line for line in block.split("\n"))
                child_nodes = [
                    ParentNode("li", [text_node_to_html_node(n) for n in text_to_textnodes(item)])
                    for item in lines
                ]
            case BlockType.PARAGRAPH:
                tag = "p"
                block = " ".join(line.strip() for line in block.split("\n"))
                child_nodes = [text_node_to_html_node(n) for n in text_to_textnodes(block)]
        rootnode.children.append(ParentNode(tag, child_nodes))
    
    return rootnode