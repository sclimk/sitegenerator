import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```
This is a code block
with multiple lines
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<pre>", html)
        self.assertIn("<code>", html)

    def test_empty_paragraph(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_nested_lists(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<ul>", html)
        self.assertIn("<li>Item 1</li>", html)
        self.assertIn("<li>Item 2</li>", html)
        self.assertIn("<li>Item 3</li>", html)

    def test_multiline_paragraph(self):
        md = """
This is a paragraph
that spans multiple
lines but should
be one <p> block.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph that spans multiple lines but should be one <p> block.</p></div>",
        )

    def test_quote_with_inline(self):
        md = """
> This is a **bold** quote
> And this is _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<blockquote>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)

    def test_code_inside_paragraph(self):
        md = """
Here is some inline `code` inside a paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<p>", html)
        self.assertIn("<code>code</code>", html)

    def test_multiple_headings(self):
        md = """
# H1
## H2
### H3
#### H4
##### H5
###### H6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        for i in range(1, 7):
            self.assertIn(f"<h{i}>H{i}</h{i}>", html)

    def test_links_and_images(self):
        md = """
Check out [Boot.dev](https://boot.dev) and this image ![alt](https://i.imgur.com/test.png)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn('<a href="https://boot.dev">Boot.dev</a>', html)
        self.assertIn('<img src="https://i.imgur.com/test.png" alt="alt" />', html)

    def test_ordered_list_with_inline(self):
        md = """
1. First **bold** item
2. Second _italic_ item
3. Third `code` item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<ol>", html)
        self.assertIn("<li>First <b>bold</b> item</li>", html)
        self.assertIn("<li>Second <i>italic</i> item</li>", html)
        self.assertIn("<li>Third <code>code</code> item</li>", html)