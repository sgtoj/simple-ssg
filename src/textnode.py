from enum import Enum


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
        self.text_type = TextType[text_type]
        self.url = url

    def __eq__(self, target):
        return (
            self.text == target.text
            and self.text_type == target.text_type
            and self.url == target.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
