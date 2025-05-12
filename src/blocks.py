import enum

from converter import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import HTMLNode


def markdown_to_blocks(markdown):
    """
    Convert markdown text to a list of blocks.
    """
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]
    return blocks

class BlockType(enum.Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unorder_list = "unorder_list"
    ordered_list = "ordered_list"
def block_to_block_type(markdown_block):
    """
    Convert a markdown block to a block type.
    """
    if any(markdown_block.startswith(f"{'#' * i} ") for i in range(1, 7)):
        return BlockType.heading
    elif markdown_block.startswith("```"):
        return BlockType.code
    elif all(line.startswith(">") for line in markdown_block.splitlines()):
        return BlockType.quote
    elif all(line.startswith("- ") for line in markdown_block.splitlines()):
        return BlockType.unorder_list
    elif is_ordered_list(markdown_block):
        return BlockType.ordered_list
    else:
        return BlockType.paragraph
    
def is_ordered_list(markdown_block):
    """
    Check if a markdown block is an ordered list.
    """
    lines = markdown_block.splitlines()
    count = 1
    for line in lines:
        if not line.startswith(f"{count}. "):
            return False
        count += 1
    return True

def markdown_to_html_node(markdown):
    blocks=markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.code:
            html_nodes.append(text_node_to_html_node(TextNode(block, TextType.CODE)))
        else:
            html_node = HTMLNode(value=block, type=block_type)
            if block_type == BlockType.heading:
                html_node.tag = "h" + str(block.count("#"))
            elif block_type == BlockType.quote:
                html_node.tag = "blockquote"
            elif block_type == BlockType.unorder_list:
                html_node.tag = "ul"
            elif block_type == BlockType.ordered_list:
                html_node.tag = "ol"
            else:
                html_node.tag = "p"
            if block_type in [BlockType.unorder_list, BlockType.ordered_list]:
                items = block.splitlines()
                html_node.children = [
                    HTMLNode(tag="li", value=item[2:]) for item in items
                ]
            elif block_type == BlockType.quote:
                html_node.children = [
                    HTMLNode(tag="p", value=item[2:]) for item in block.splitlines()
                ]
            elif block_type == BlockType.paragraph:
                html_node.children = [
                    text_node_to_html_node(TextNode(item, TextType.TEXT))
                    for item in block.splitlines()
                ]
            elif block_type == BlockType.heading:
                html_node.children = [
                    text_node_to_html_node(TextNode(item, TextType.TEXT))
                    for item in block.splitlines()
                ]
        
            html_nodes.append(html_node)
    return html_nodes