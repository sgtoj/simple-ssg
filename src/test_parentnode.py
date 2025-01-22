import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_with_few_children(self):
        children = [
            LeafNode("p", "item 1"),
            LeafNode("p", "item 2"),
            LeafNode("p", "item 3"),
        ]
        node = ParentNode("div", children, {"class": "foobar"})
        expected_html = (
            '<div class="foobar"><p>item 1</p><p>item 2</p><p>item 3</p></div>'
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_with_nested_parent_and_children(self):
        d1_children = [
            LeafNode("p", "inner item 1"),
            LeafNode("p", "inner item 2"),
            LeafNode("p", "inner item 3"),
        ]
        d1_node = ParentNode("div", d1_children, {"class": "inner"})
        d0_children = [
            LeafNode("p", "item 1"),
            LeafNode("p", "item 2"),
            LeafNode("p", "item 3"),
            d1_node,
        ]
        d0_node = ParentNode("div", d0_children, {"class": "outter"})
        expected_html = '<div class="outter"><p>item 1</p><p>item 2</p><p>item 3</p><div class="inner"><p>inner item 1</p><p>inner item 2</p><p>inner item 3</p></div></div>'
        self.assertEqual(d0_node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
