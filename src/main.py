from os_utils import copy_src_dir_to_dst_dir
from page_generator import generate_page, generate_pages_recursive
from textnode import TextNode, TextType
import sys

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_src_dir_to_dst_dir("static","docs")
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="docs",
        basepath=basepath
    )
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="docs/index.html",
        basepath=basepath
    )


if __name__ == "__main__":
    main()
