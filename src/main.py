from textnode import TextNode

if __name__ == "__main__":
    text_node = TextNode("This is a text node", "S_BOLD", "https://www.boot.dev")
    print(text_node)
    print(
        text_node == TextNode("This is a text node", "S_BOLD", "https://www.boot.dev")
    )
