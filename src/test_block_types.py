import unittest
from block_types import BlockType, block_to_block_type

class TestBlockTypes(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Hello"),
            BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("###### Six levels"),
            BlockType.HEADING
        )

    def test_not_heading_no_space(self):
        # "#NoSpace" is NOT a heading ? paragraph
        self.assertEqual(
            block_to_block_type("#NoSpace"),
            BlockType.PARAGRAPH
        )

    def test_code_block(self):
        block = """```
print("hello")
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> quote line\n> another line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_numbers(self):
        block = "1. first\n3. wrong number"
        # Wrong numbering ? paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a regular paragraph."),
            BlockType.PARAGRAPH
        )


if __name__ == "__main__":
    unittest.main()