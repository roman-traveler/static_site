from htmlnode import LeafNode
from splitting_utils import split_nodes_delimiter, split_nodes_link, split_nodes_image
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception("Unindentified text type")


def text_to_textnodes(text: str):
    """
    Convert a string to a list of text nodes.
    """
    text = [TextNode(text, TextType.TEXT)]
    text = split_nodes_delimiter(text, "**", TextType.BOLD)

    text = split_nodes_delimiter(text, "_", TextType.ITALIC)

    text = split_nodes_delimiter(text, "`", TextType.CODE)
    return split_nodes_link(split_nodes_image(text))
