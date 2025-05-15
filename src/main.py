from os_utils import copy_src_dir_to_dst_dir
from textnode import TextNode, TextType


def main():
    a = TextNode("a", TextType.BOLD, "https://www.boot.dev")
    copy_src_dir_to_dst_dir("static","public")
    print(a)


if __name__ == "__main__":
    main()
