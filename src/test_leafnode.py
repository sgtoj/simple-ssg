import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        props_expected_str = 'href="https://www.google.com" target="_blank"'
        node = LeafNode("div", "click here", props)
        self.assertEqual(node.props_to_html(), props_expected_str)

    def test_values(self):
        node = LeafNode("div", "you shall not pass")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "you shall not pass")
        self.assertEqual(node.props, {})

    def test__repr__(self):
        props = {"class": "bruh"}
        node = LeafNode("p", "wat up", props)
        self.assertEqual(str(node), 'HTMLNode(p, wat up, [], class="bruh")')

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


if __name__ == "__main__":
    unittest.main()
