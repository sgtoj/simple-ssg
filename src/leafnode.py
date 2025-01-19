from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value == None:
            raise ValueError("value cannot be `None` type")
        if self.tag == "":
            return self.value
        tag_with_props = " ".join([self.tag, self.props_to_html()]).strip()
        return f"<{tag_with_props}>{self.value}</{self.tag}>"
