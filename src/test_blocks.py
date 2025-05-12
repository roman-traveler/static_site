from blocks import markdown_to_blocks, block_to_block_type, BlockType, is_ordered_list, markdown_to_html_node
import unittest


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_no_newline(self):
        md = "This is a single line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line"])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.heading)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.heading)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.code)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.quote)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.quote)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.unorder_list)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ordered_list)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.paragraph)


class TestIsOrderedList(unittest.TestCase):
    def test_valid_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertTrue(is_ordered_list(markdown))

    def test_invalid_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2\n- Item 3"
        self.assertFalse(is_ordered_list(markdown))

    def test_non_ordered_list(self):
        markdown = "- Item 1\n- Item 2"
        self.assertFalse(is_ordered_list(markdown))

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
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

if __name__ == "__main__":
    unittest.main()
