from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from convert import text_node_to_html_node
from text_to_textnodes import text_to_textnodes
from block_types import BlockType, block_to_block_type
from markdown_to_blocks import markdown_to_blocks

def paragraph_to_html(block):
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_html(block):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    text = block[level+1:]   # skip '# ' characters
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def codeblock_to_html(block):
    stripped = block[3:-3]  # remove starting and ending ```
    code_node = ParentNode("code", [LeafNode(stripped, "text")])
    return ParentNode("pre", [code_node])

def quote_to_html(block):
    lines = [line[1:].lstrip() for line in block.split("\n")]
    text = "\n".join(lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def unordered_list_to_html(block):
    li_nodes = []
    for line in block.split("\n"):
        item_text = line[2:]   # remove "- "
        children = text_to_children(item_text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)

def ordered_list_to_html(block):
    li_nodes = []
    lines = block.split("\n")
    for line in lines:
        # remove "n. "
        item_text = line.split(". ", 1)[1]
        children = text_to_children(item_text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)

def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html(block)
    if block_type == BlockType.HEADING:
        return heading_to_html(block)
    if block_type == BlockType.CODE:
        return codeblock_to_html(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html(block)
    raise ValueError("Unknown block type")

from convert import text_node_to_html_node
from text_to_textnodes import text_to_textnodes

def text_to_children(text: str):
    """
    Converts raw text with inline markdown into a list of HTMLNode children.
    """
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        bt = block_to_block_type(block)
        html_block = block_to_html_node(block, bt)
        children.append(html_block)

    return ParentNode("div", children)