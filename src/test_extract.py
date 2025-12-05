import unittest
from extract import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_multiple_images(self):
        text = (
            "Look ![one](url1.png) and ![two](url2.jpg) wow!"
        )
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("one", "url1.png"), ("two", "url2.jpg")],
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Go to [Google](https://google.com)"
        )
        self.assertListEqual(
            [("Google", "https://google.com")],
            matches
        )

    def test_extract_multiple_links(self):
        text = (
            "Links: [A](u1) and [B](u2)"
        )
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("A", "u1"), ("B", "u2")],
            matches
        )

    def test_links_do_not_match_images(self):
        text = "![img](url1) and [link](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("link", "url2")],
            matches
        )

    def test_no_matches(self):
        self.assertListEqual(extract_markdown_images("no images"), [])
        self.assertListEqual(extract_markdown_links("no links"), [])