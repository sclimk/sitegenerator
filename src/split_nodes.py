import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Existing helper you already used. Keeps behavior the same.
    """
    new_nodes = []

    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        parts = text.split(delimiter)

        # If there is an even number of segments, delimiters are unbalanced
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {text}")

        # Build new nodes
        for i, segment in enumerate(parts):
            if segment == "":
                continue

            if i % 2 == 0:
                # Outside delimiters ? regular text
                new_nodes.append(TextNode(segment, TextType.TEXT))
            else:
                # Inside delimiters ? specified formatted type
                new_nodes.append(TextNode(segment, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    """
    Split TextType.TEXT nodes into image nodes and text nodes based on markdown
    image syntax: ![alt](url)

    Returns a new list of TextNode objects.
    """
    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')  # capture alt and url
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        matches = list(pattern.finditer(text))

        if not matches:
            new_nodes.append(node)
            continue

        for m in matches:
            start, end = m.span()
            alt = m.group(1)
            url = m.group(2)

            # text before match
            if start > last_index:
                before = text[last_index:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))

            # the image node
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            last_index = end

        # trailing text after last match
        if last_index < len(text):
            trailing = text[last_index:]
            if trailing:
                new_nodes.append(TextNode(trailing, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextType.TEXT nodes into link nodes and text nodes based on markdown
    link syntax: [text](url), but NOT images (which start with !).
    Returns a new list of TextNode objects.
    """
    # negative lookbehind ensures we don't match images prefixed with '!'
    pattern = re.compile(r'(?<!\!)\[(.*?)\]\((.*?)\)')
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        matches = list(pattern.finditer(text))

        if not matches:
            new_nodes.append(node)
            continue

        for m in matches:
            start, end = m.span()
            anchor = m.group(1)
            url = m.group(2)

            # text before match
            if start > last_index:
                before = text[last_index:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))

            # the link node
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

            last_index = end

        # trailing text after last match
        if last_index < len(text):
            trailing = text[last_index:]
            if trailing:
                new_nodes.append(TextNode(trailing, TextType.TEXT))

    return new_nodes