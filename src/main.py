from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.S_NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.S_BOLD:
            return LeafNode("b", text_node.text)
        case TextType.S_ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.S_CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    raise Exception("unknown text type")


if __name__ == "__main__":
    text_node = TextNode("This is a text node", TextType.S_BOLD, "https://www.boot.dev")
    print(text_node)
    print(
        text_node
        == TextNode("This is a text node", TextType.S_BOLD, "https://www.boot.dev")
    )
