from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    S_NORMAL = "S_NORMAL"
    S_BOLD = "S_BOLD"
    S_ITALIC = "S_ITALIC"
    S_CODE = "S_CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target):
        return (
            self.text == target.text
            and self.text_type == target.text_type
            and self.url == target.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: "TextNode"):
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
