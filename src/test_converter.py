import unittest

from textnode import TextNode, TextType
from converter import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_normal_code(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(text_node_to_html_node(node).to_html(), "This is a text node")

    def test_bold_code(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            text_node_to_html_node(node).to_html(), "<b>This is a text node</b>"
        )

    def test_italic_code(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(
            text_node_to_html_node(node).to_html(), "<i>This is a text node</i>"
        )

    def test_code_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(
            text_node_to_html_node(node).to_html(), "<code>This is a text node</code>"
        )

    def test_link_code_no_link(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(
            text_node_to_html_node(node).to_html(), "<a >This is a text node</a>"
        )

    def test_image_code_no_link(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<img alt="This is a text node"></img>',
        )

    def test_link_code(self):
        node = TextNode("This is a text node", TextType.LINK, url="abc")
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<a href="abc">This is a text node</a>',
        )

    def test_image_code(self):
        node = TextNode("This is a text node", TextType.IMAGE, url="abc")
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<img src="abc" alt="This is a text node"></img>',
        )

    def test_unknown_code(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node.text_type = "Unknown"
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
