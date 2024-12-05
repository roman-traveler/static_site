import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    reforged_lines=[]
    for line in old_nodes:
        lines = line.text.split(delimiter)
        is_delimited=False
        for l in lines:
            if is_delimited:
                reforged_lines.append(TextNode(l, text_type))
            else:
                reforged_lines.append(TextNode(l, line.text_type))
            is_delimited = not(is_delimited)
    return reforged_lines

def extract_markdown_images(text):
    val = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return val
def extract_markdown_links(text):
    val = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return val

def split_nodes_image(old_nodes):
    pass

def split_nodes_link(old_nodes):
    pass