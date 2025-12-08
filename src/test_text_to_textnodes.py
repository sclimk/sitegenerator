import unittest

from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an " \
               "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a " \
               "[link](https://boot.dev)"

        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(nodes, expected)

    def test_only_text(self):
        nodes = text_to_textnodes("hello world")
        self.assertEqual(nodes, [TextNode("hello world", TextType.TEXT)])

    def test_mix_bold_and_link(self):
        text = "**bold** and a [site](https://example.com)"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and a ", TextType.TEXT),
            TextNode("site", TextType.LINK, "https://example.com"),
        ]

        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()