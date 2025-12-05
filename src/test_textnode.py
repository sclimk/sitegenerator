import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_equal_text(self):
        node = TextNode("hello", TextType.TEXT)
        node2 = TextNode("goodbye", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_equal_text_type(self):
        node = TextNode("same text", TextType.BOLD)
        node2 = TextNode("same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_default_none(self):
        node = TextNode("test", TextType.LINK)
        self.assertIsNone(node.url)

    def test_equal_with_url(self):
        node = TextNode("click me", TextType.LINK, "https://example.com")
        node2 = TextNode("click me", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
