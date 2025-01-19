from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("tag propery cannot be `None` type or empty")
        if len(self.children) == 0:
            raise ValueError("parent node has no children")
        children_html = "".join(map(lambda x: x.to_html(), self.children))
        tag_with_props = " ".join([self.tag, self.props_to_html()]).strip()
        return f"<{tag_with_props}>{children_html}</{self.tag}>"
