import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_props(self):
        node = HTMLNode(tag="a", value="Click me", props={"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p", value="Hello world")
        # props is None by default, should return empty string
        self.assertEqual(node.props_to_html(), "")

    def test_repr_shows_all_members(self):
        child = HTMLNode(tag="span", value="hello")
        parent = HTMLNode(tag="p", children=[child], props={"class": "text"})
        repr_str = repr(parent)
        # Check that repr contains all important info
        self.assertIn("tag='p'", repr_str)
        self.assertIn("children=[HTMLNode(tag='span'", repr_str)
        self.assertIn("props={'class': 'text'}", repr_str)

if __name__ == "__main__":
    unittest.main()