import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.S_BOLD)
        node2 = TextNode("This is a text node", TextType.S_BOLD)
        node3 = TextNode("This is a text node", TextType.S_NORMAL)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_normal(self):
        node = text_node_to_html_node(
            TextNode("this is a text node", TextType.S_NORMAL),
        )
        self.assertEqual(node.tag, "")
        self.assertEqual(node.value, "this is a text node")

    def test_bold(self):
        node = text_node_to_html_node(
            TextNode("this is a text node", TextType.S_BOLD),
        )
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "this is a text node")

    def test_italic(self):
        node = text_node_to_html_node(
            TextNode("this is a text node", TextType.S_ITALIC),
        )
        self.assertEqual(node.tag, "i")
        self.assertEqual(node.value, "this is a text node")

    def test_image(self):
        node = text_node_to_html_node(
            TextNode("this is a text node", TextType.IMAGE, "https://github.com"),
        )
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(
            node.props, {"src": "https://github.com", "alt": "this is a text node"}
        )


class TestTextSplitNodeDelimiter(unittest.TestCase):
    def test_bold(self):
        input_nodes = [
            TextNode("this is a **text** node", TextType.S_NORMAL),
        ]
        output_nodes = split_nodes_delimiter(input_nodes, "**", TextType.S_BOLD)
        expected_nodes = [
            TextNode("this is a ", TextType.S_NORMAL),
            TextNode("text", TextType.S_BOLD),
            TextNode(" node", TextType.S_NORMAL),
        ]
        self.assertEqual(output_nodes, expected_nodes)

    def test_italic(self):
        input_nodes = [
            TextNode("this is a *text* node", TextType.S_NORMAL),
        ]
        output_nodes = split_nodes_delimiter(input_nodes, "*", TextType.S_ITALIC)
        expected_nodes = [
            TextNode("this is a ", TextType.S_NORMAL),
            TextNode("text", TextType.S_ITALIC),
            TextNode(" node", TextType.S_NORMAL),
        ]
        self.assertEqual(output_nodes, expected_nodes)

    def test_italic_and_bold(self):
        input_nodes = [
            TextNode("*this* is a **text** node", TextType.S_NORMAL),
        ]
        output_nodes = split_nodes_delimiter(input_nodes, "**", TextType.S_BOLD)
        output_nodes = split_nodes_delimiter(output_nodes, "*", TextType.S_ITALIC)
        expected_nodes = [
            TextNode("this", TextType.S_ITALIC),
            TextNode(" is a ", TextType.S_NORMAL),
            TextNode("text", TextType.S_BOLD),
            TextNode(" node", TextType.S_NORMAL),
        ]
        self.assertEqual(output_nodes, expected_nodes)


class TestTextSplitNodeLinks(unittest.TestCase):
    def test_bold(self):
        input_nodes = [
            TextNode(
                "this is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.S_NORMAL,
            ),
        ]
        output_nodes = split_nodes_link(input_nodes)
        expected_nodes = [
            TextNode("this is text with a link ", TextType.S_NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.S_NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(output_nodes, expected_nodes)


class TestTextSplitNodeImages(unittest.TestCase):
    def test_bold(self):
        input_nodes = [
            TextNode(
                "this has a image for ![boot dev](https://www.boot.dev) and to ![youtube](https://www.youtube.com/@bootdotdev)",
                TextType.S_NORMAL,
            ),
        ]
        output_nodes = split_nodes_image(input_nodes)
        expected_nodes = [
            TextNode("this has a image for ", TextType.S_NORMAL),
            TextNode("boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and to ", TextType.S_NORMAL),
            TextNode("youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(output_nodes, expected_nodes)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_multiple(self):
        input = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image_details = extract_markdown_images(input)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(image_details, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_multiple(self):
        input = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        image_details = extract_markdown_links(input)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(image_details, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_fn(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.S_NORMAL),
            TextNode("text", TextType.S_BOLD),
            TextNode(" with an ", TextType.S_NORMAL),
            TextNode("italic", TextType.S_ITALIC),
            TextNode(" word and a ", TextType.S_NORMAL),
            TextNode("code block", TextType.S_CODE),
            TextNode(" and an ", TextType.S_NORMAL),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.S_NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()
