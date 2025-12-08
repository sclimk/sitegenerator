# src/test_split_images_links.py
import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_image, split_nodes_link

class TestSplitImagesLinks(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_at_start_and_end(self):
        node = TextNode(
            "![start](s.png) middle ![end](e.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "s.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "e.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_no_match(self):
        node = TextNode("no images here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_and_images_mixed(self):
        # Make sure link splitting doesn't touch images and vice versa
        node = TextNode(
            "![img](i.png) and [link](u)",
            TextType.TEXT,
        )
        # splitting links only should leave image as raw text (image stays as markdown text)
        # but because split_nodes_link only operates on TextType.TEXT and uses negative lookbehind,
        # it will not convert the image, so we expect first node to be text up to the image
        # Actually better to run both: first images, then links
        step1 = split_nodes_image([node])
        step2 = split_nodes_link(step1)
        expected = [
            TextNode("", TextType.TEXT),  # If there is empty text before image it may be skipped; depends on implementation
        ]
        # Instead assert correct structure after both operations:
        final = step2
        self.assertEqual(final[0].text, "img")
        self.assertEqual(final[0].text_type, TextType.IMAGE)
        self.assertEqual(final[0].url, "i.png")
        # link should be present later
        found_link = any(n.text_type == TextType.LINK and n.url == "u" for n in final)
        self.assertTrue(found_link)

    def test_split_links_adjacent(self):
        node = TextNode("[a](u1)[b](u2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("a", TextType.LINK, "u1"),
            TextNode("b", TextType.LINK, "u2"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_unmatched_not_applicable(self):
        # Our image/link regex won't match unmatched patterns, so we don't raise here.
        node = TextNode("bad ![image(", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

if __name__ == "__main__":
    unittest.main()