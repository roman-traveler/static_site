class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        pairs = [
            attribute + '="' + value + '"'
            for attribute, value in self.props.items()
            if value is not None
        ]
        return " " + " ".join(pairs)

    def __repr__(self):
        return "\n".join(
            "tag: " + self.tag,
            "value: " + self.value,
            "children" + self.children,
            "props: " + self.props,
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        opening_tag = "<" + self.tag + self.props_to_html() + ">"
        closing_tag = "</" + self.tag + ">"
        return opening_tag + self.value + closing_tag


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("missing tag")
        if self.children is None:
            raise ValueError("No children - use another htmltag type")
        opening_tag = "<" + self.tag + self.props_to_html() + ">"
        closing_tag = "</" + self.tag + ">"
        return (
            opening_tag
            + "".join([child.to_html() for child in self.children])
            + closing_tag
        )
