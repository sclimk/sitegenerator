from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    # ------------------------
    # Heading
    # ------------------------
    # 1�6 '#' characters followed by a space
    if lines[0].startswith("#"):
        i = 0
        while i < len(lines[0]) and lines[0][i] == "#":
            i += 1
        if 1 <= i <= 6 and len(lines[0]) > i and lines[0][i] == " ":
            return BlockType.HEADING

    # ------------------------
    # Code block
    # ------------------------
    # must start AND end with ```
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    # ------------------------
    # Quote block
    # ------------------------
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # ------------------------
    # Unordered list
    # ------------------------
    # Every line: "- something"
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ------------------------
    # Ordered list
    # ------------------------
    # Lines: "1. item", "2. item", etc.
    ordered = True
    for i, line in enumerate(lines):
        prefix = f"{i+1}. "
        if not line.startswith(prefix):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST

    # ------------------------
    # Default: paragraph
    # ------------------------
    return BlockType.PARAGRAPH