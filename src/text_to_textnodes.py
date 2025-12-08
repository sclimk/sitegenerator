from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    # Bold first
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Italic next (your project probably uses "_")
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Images
    nodes = split_nodes_image(nodes)

    # Links
    nodes = split_nodes_link(nodes)

    return nodes