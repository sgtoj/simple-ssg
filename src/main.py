from leafnode import LeafNode
from textnode import TextNode, TextType

if __name__ == "__main__":
    text_node = TextNode("This is a text node", TextType.S_BOLD, "https://www.boot.dev")
    print(text_node)
    print(
        text_node
        == TextNode("This is a text node", TextType.S_BOLD, "https://www.boot.dev")
    )
