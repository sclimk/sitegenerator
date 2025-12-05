import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("a", "Link", {"href": "https://example.com", "target": "_blank"})
        expected = '<a href="https://example.com" target="_blank">Link</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_missing_value_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

if __name__ == "__main__":
    unittest.main()