import unittest
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_simple_code(self):
        node = TextNode("This is `code` here", TextType.TEXT)
        new = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new), 3)
        self.assertEqual(new[0].text, "This is ")
        self.assertEqual(new[0].text_type, TextType.TEXT)

        self.assertEqual(new[1].text, "code")
        self.assertEqual(new[1].text_type, TextType.CODE)

        self.assertEqual(new[2].text, " here")
        self.assertEqual(new[2].text_type, TextType.TEXT)

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new[1].text_type, TextType.BOLD)
        self.assertEqual(new[1].text, "bold")

    def test_italic(self):
        node = TextNode("That is _italic_ text", TextType.TEXT)
        new = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new[1].text_type, TextType.ITALIC)

    def test_no_split(self):
        node = TextNode("nothing special here", TextType.TEXT)
        new = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new), 1)
        self.assertEqual(new[0].text, "nothing special here")

    def test_unmatched_delimiter(self):
        node = TextNode("bad `markdown", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

if __name__ == "__main__":
    unittest.main()