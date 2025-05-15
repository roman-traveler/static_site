from os_utils import copy_src_dir_to_dst_dir
from page_generator import generate_page
from textnode import TextNode, TextType


def main():
    copy_src_dir_to_dst_dir("static","public")
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )


if __name__ == "__main__":
    main()
