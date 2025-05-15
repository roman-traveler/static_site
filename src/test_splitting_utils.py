import unittest
from splitting_utils import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplit(unittest.TestCase):
    def test_single_item(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            repr(new_nodes),
            "[TextNode(This is text with a , normal, None), TextNode(code block, code, None), TextNode( word, normal, None)]",
        )

    def test_multiple_same_type(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a `different` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            repr(new_nodes),
            "[TextNode(This is text with a , normal, None), TextNode(code block, code, None), TextNode( word, normal, None), TextNode(This is text with a , normal, None), TextNode(different, code, None), TextNode( word, normal, None)]",
        )

    def test_mismatch(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1], "*", TextType.CODE)
        self.assertEqual(
            repr(new_nodes),
            "[TextNode(This is text with a `code block` word, normal, None)]",
        )


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images_basic(self):
        """Test basic extraction of markdown images."""
        text = "![Alt text](http://example.com/image.png)"
        expected = [("Alt text", "http://example.com/image.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_multiple(self):
        """Test extraction of multiple markdown images."""
        text = (
            "First image ![Image One](http://example.com/one.png) "
            "and second image ![Image Two](http://example.com/two.png)"
        )
        expected = [
            ("Image One", "http://example.com/one.png"),
            ("Image Two", "http://example.com/two.png"),
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_no_images(self):
        """Test text with no markdown images."""
        text = "This is a text without any images."
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_nested(self):
        """Test extraction when images have nested brackets or parentheses."""
        text = "![An image [with] brackets](http://example.com/image.png)"
        expected = [("An image [with] brackets", "http://example.com/image.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_malformed(self):
        """Test extraction with malformed markdown image syntax."""
        text = "![Missing closing parenthesis](http://example.com/image.png"
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_special_characters(self):
        """Test extraction with special characters in alt text and URL."""
        text = "![Alt text with !@#$%^&*()](http://example.com/image.png?param=value&other=üñîçødé)"
        expected = [
            (
                "Alt text with !@#$%^&*()",
                "http://example.com/image.png?param=value&other=üñîçødé",
            )
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_basic(self):
        """Test basic extraction of markdown links."""
        text = "[Link text](http://example.com)"
        expected = [("Link text", "http://example.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple(self):
        """Test extraction of multiple markdown links."""
        text = (
            "First link [Link One](http://example.com/one) "
            "and second link [Link Two](http://example.com/two)"
        )
        expected = [
            ("Link One", "http://example.com/one"),
            ("Link Two", "http://example.com/two"),
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_no_links(self):
        """Test text with no markdown links."""
        text = "This is a text without any links."
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_nested(self):
        """Test extraction when links have nested brackets or parentheses."""
        text = "[A link [with] brackets](http://example.com)"
        expected = [("A link [with] brackets", "http://example.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_malformed(self):
        """Test extraction with malformed markdown link syntax."""
        text = "[Missing closing parenthesis](http://example.com"
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_special_characters(self):
        """Test extraction with special characters in link text and URL."""
        text = (
            "[Link text with !@#$%^&*()](http://example.com?param=value&other=üñîçødé)"
        )
        expected = [
            (
                "Link text with !@#$%^&*()",
                "http://example.com?param=value&other=üñîçødé",
            )
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_links_mixed(self):
        """Test extraction when images and links are mixed in text."""
        text = (
            "Here is an image ![Image](http://example.com/image.png) "
            "and a link [Link](http://example.com)."
        )
        expected_images = [("Image", "http://example.com/image.png")]
        expected_links = expected_images + [("Link", "http://example.com")]
        result_images = extract_markdown_images(text)
        result_links = extract_markdown_links(text)
        self.assertEqual(result_images, expected_images)
        self.assertEqual(result_links, expected_links)

    def test_extract_markdown_links_empty_text(self):
        """Test extraction with empty link text."""
        text = "[]()"
        expected = [("", "")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_empty_alt_and_url(self):
        """Test extraction with empty alt text and URL in image."""
        text = "![]()"
        expected = [("", "")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_only_brackets(self):
        """Test extraction when text contains only brackets."""
        text = "[]"
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_only_exclamation_brackets(self):
        """Test extraction when text contains only exclamation and brackets."""
        text = "![Alt text]"
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

        class TestExtractTitle(unittest.TestCase):
            def test_extract_title_basic(self):
                """Test extraction of a basic markdown title."""
                markdown = "# This is a title"
                expected = "This is a title"
                result = extract_title(markdown)
                self.assertEqual(result, expected)

            def test_extract_title_with_extra_text(self):
                """Test extraction of a title with extra text below."""
                markdown = "# Title\nSome other text"
                expected = "Title"
                result = extract_title(markdown)
                self.assertEqual(result, expected)

            def test_extract_title_with_leading_whitespace(self):
                """Test extraction of a title with leading whitespace."""
                markdown = "   # Title with leading spaces"
                expected = "Title with leading spaces"
                result = extract_title(markdown)
                self.assertEqual(result, expected)

            def test_extract_title_no_title(self):
                """Test extraction when no title is present."""
                markdown = "This is text without a title"
                with self.assertRaises(ValueError) as context:
                    extract_title(markdown)
                self.assertEqual(str(context.exception), "invalid markdown, title not found")

            def test_extract_title_multiple_titles(self):
                """Test extraction when multiple titles are present."""
                markdown = "# First Title\n# Second Title"
                expected = "First Title"
                result = extract_title(markdown)
                self.assertEqual(result, expected)

            def test_extract_title_empty_string(self):
                """Test extraction when the markdown is an empty string."""
                markdown = ""
                with self.assertRaises(ValueError) as context:
                    extract_title(markdown)
                self.assertEqual(str(context.exception), "invalid markdown, title not found")

            def test_extract_title_special_characters(self):
                """Test extraction of a title with special characters."""
                markdown = "# Title with !@#$%^&*()"
                expected = "Title with !@#$%^&*()"
                result = extract_title(markdown)
                self.assertEqual(result, expected)

            def test_extract_title_with_trailing_whitespace(self):
                """Test extraction of a title with trailing whitespace."""
                markdown = "# Title with trailing spaces   "
                expected = "Title with trailing spaces"
                result = extract_title(markdown)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
