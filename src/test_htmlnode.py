import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        props_expected_str = 'href="https://www.google.com" target="_blank"'
        node = HTMLNode("div", "click here", None, props)
        self.assertEqual(node.props_to_html(), props_expected_str)

    def test_values(self):
        node = HTMLNode("div", "you shall not pass")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "you shall not pass")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test__repr__(self):
        props = {"class": "bruh"}
        node = HTMLNode("p", "wat up", None, props)
        self.assertEqual(str(node), 'HTMLNode(p, wat up, [], class="bruh")')


if __name__ == "__main__":
    unittest.main()
