from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        parts = text.split(delimiter)

        # If there is an odd number of segments, the delimiters are unbalanced
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