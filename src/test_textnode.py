import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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


if __name__ == "__main__":
    unittest.main()
