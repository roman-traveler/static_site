import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_one_props_to_html(self):
        node = HTMLNode("p", "example paragraph", props={"color": "red"})
        self.assertEqual(node.props_to_html(), ' color="red"')

    def test_multi_props_to_html(self):
        node = HTMLNode(
            "p", "example paragraph", props={"color": "red", "font": "colibri"}
        )
        self.assertEqual(node.props_to_html(), ' color="red" font="colibri"')

    def test_no_props_to_html(self):
        node = HTMLNode("p", "example paragraph")
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_one_props_to_html(self):
        node = LeafNode("p", "example paragraph", props={"color": "red"})
        self.assertEqual(node.to_html(), '<p color="red">example paragraph</p>')

    def test_multi_props_to_html(self):
        node = LeafNode(
            "p", "example paragraph", props={"color": "red", "font": "colibri"}
        )
        self.assertEqual(
            node.to_html(), '<p color="red" font="colibri">example paragraph</p>'
        )

    def test_no_props_to_html(self):
        node = LeafNode("p", "example paragraph")
        self.assertEqual(node.to_html(), "<p>example paragraph</p>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        """Test ParentNode to_html with children."""
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        node = ParentNode(tag="div", children=[child1, child2])
        expected_html = "<div><span>Child 1</span><span>Child 2</span></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_props(self):
        """Test ParentNode to_html with properties."""
        child = LeafNode(tag="p", value="Paragraph")
        node = ParentNode(tag="div", children=[child], props={"class": "container"})
        expected_html = '<div class="container"><p>Paragraph</p></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_no_tag(self):
        """Test ParentNode to_html with no tag; should raise ValueError."""
        child = LeafNode(tag="p", value="Paragraph")
        node = ParentNode(tag=None, children=[child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        """Test ParentNode to_html with no children; should raise ValueError."""
        node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children(self):
        """Test ParentNode to_html with empty children list."""
        node = ParentNode(tag="div", children=[])
        expected_html = "<div></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_nested_parent_nodes(self):
        """Test ParentNode with nested ParentNodes."""
        inner_child = LeafNode(tag="span", value="Inner Child")
        inner_parent = ParentNode(
            tag="div", children=[inner_child], props={"class": "inner"}
        )
        outer_parent = ParentNode(
            tag="section", children=[inner_parent], props={"class": "outer"}
        )
        expected_html = '<section class="outer"><div class="inner"><span>Inner Child</span></div></section>'
        self.assertEqual(outer_parent.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
