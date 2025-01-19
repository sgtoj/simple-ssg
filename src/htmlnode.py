class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag or ""
        self.value = value or ""
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        return " ".join(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
