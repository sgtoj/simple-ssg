import re
from enum import Enum
from leafnode import LeafNode

REGEXP_MD_IMAGE_PARTS = r"!\[(.*?)\]\((.*?)\)"
REGEXP_MD_IMAGE_FULL = r"(!\[.*?\]\(.*?\))"
REGEXP_MD_LINK_PARTS = r"\[(.*?)\]\((.*?)\)"
REGEXP_MD_LINK_FULL = r"(\[.*?\]\(.*?\))"


class TextType(Enum):
    S_NORMAL = "S_NORMAL"
    S_BOLD = "S_BOLD"
    S_ITALIC = "S_ITALIC"
    S_CODE = "S_CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"


class TextNode:
    def __init__(self, text: str, text_type: "TextType", url: str | None = None):
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


def text_node_to_html_node(text_node: "TextNode") -> "LeafNode":
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
        case _:
            raise Exception("unknown text type")


def text_to_textnodes(text: str) -> "list[TextNode]":
    nodes = [TextNode(text, TextType.S_NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.S_BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.S_ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.S_CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(
    old_nodes: "list[TextNode]", delimiter: "str", text_type: "TextType"
) -> "list[TextNode]":
    new_nodes: "list[TextNode]" = []
    for node in old_nodes:
        if node.text_type != TextType.S_NORMAL:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown")
        split_nodes: list[TextNode] = []
        for i in range(0, len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.S_NORMAL))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(nodes: "list[TextNode]") -> "list[TextNode]":
    new_nodes: "list[TextNode]" = []
    for node in nodes:
        if node.text_type != TextType.S_NORMAL:
            new_nodes.append(node)
            continue
        parts = re.split(REGEXP_MD_LINK_FULL, node.text)
        split_nodes: list[TextNode] = []
        for i in range(0, len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.S_NORMAL))
            else:
                link_data = extract_markdown_link(parts[i])
                split_nodes.append(TextNode(link_data[0], TextType.LINK, link_data[1]))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(nodes: "list[TextNode]") -> "list[TextNode]":
    new_nodes: "list[TextNode]" = []
    for node in nodes:
        if node.text_type != TextType.S_NORMAL:
            new_nodes.append(node)
            continue
        parts = re.split(REGEXP_MD_IMAGE_FULL, node.text)
        split_nodes: list[TextNode] = []
        for i in range(0, len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.S_NORMAL))
            else:
                img_data = extract_markdown_image(parts[i])
                split_nodes.append(TextNode(img_data[0], TextType.IMAGE, img_data[1]))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = REGEXP_MD_IMAGE_PARTS
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_image(text: str) -> tuple[str, str]:
    matches = extract_markdown_images(text)
    return matches[0]


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = REGEXP_MD_LINK_PARTS
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_link(text: str) -> tuple[str, str]:
    matches = extract_markdown_links(text)
    return matches[0]
