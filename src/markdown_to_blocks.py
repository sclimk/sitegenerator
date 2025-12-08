import re

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    current_block = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
            continue

        # Start a new block for headings
        if re.match(r"^#{1,6} ", stripped):
            if current_block:
                blocks.append("\n".join(current_block))
            blocks.append(stripped)
            current_block = []
        else:
            current_block.append(stripped)

    if current_block:
        blocks.append("\n".join(current_block))

    return blocks