import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_leaf_children(self):
        children = [
            LeafNode("b", "Bold"),
            LeafNode(None, "Normal"),
            LeafNode("i", "Italic"),
        ]
        parent_node = ParentNode("p", children)
        self.assertEqual(parent_node.to_html(), "<p><b>Bold</b>Normal<i>Italic</i></p>")

    def test_nested_parent_nodes(self):
        inner_child = LeafNode("em", "inner")
        inner_parent = ParentNode("span", [inner_child])
        outer_parent = ParentNode("div", [inner_parent])
        self.assertEqual(outer_parent.to_html(), "<div><span><em>inner</em></span></div>")

    def test_parent_with_props(self):
        child = LeafNode("b", "Bold")
        parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        expected = '<div class="container" id="main"><b>Bold</b></div>'
        self.assertEqual(parent.to_html(), expected)

    def test_missing_tag_raises(self):
        child = LeafNode("b", "Bold")
        with self.assertRaises(ValueError):
            ParentNode(None, [child])

    def test_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

if __name__ == "__main__":
    unittest.main()