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
        # join each key="value" pair with a space and add a leading space
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r})"
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        self_closing_tags = {"img", "br", "hr", "input", "meta", "link"}

        if self.tag is None:
            if self.value is None:
                raise ValueError("LeafNode must have a value if tag is None")
            return str(self.value)

        # Self-closing tag
        if self.tag in self_closing_tags:
            return f"<{self.tag}{self.props_to_html()} />"

        # Normal tag requires a value
        if self.value is None:
            raise ValueError("LeafNode must have a value for non-self-closing tags")
        
        # This will include any props correctly
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")

        # Recursively call to_html on each child and concatenate
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
