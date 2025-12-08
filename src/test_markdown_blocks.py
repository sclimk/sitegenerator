import unittest
from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = "Just a single paragraph, no splits here."
        self.assertEqual(markdown_to_blocks(md), ["Just a single paragraph, no splits here."])

    def test_extra_blank_lines(self):
        md = """

Paragraph one


Paragraph two



Paragraph three

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Paragraph one", "Paragraph two", "Paragraph three"]
        )


if __name__ == "__main__":
    unittest.main()