from textnode import TextNode, TextType

def main():
    a = TextNode("a", TextType.BOLD, "https://www.boot.dev")
    print(a)

if __name__ == "__main__":
    main()