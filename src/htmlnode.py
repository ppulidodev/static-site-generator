

class HTMLNode():

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return " ".join(f'{key}="{value}"' for key, value in self.props.items()).strip()
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and 
                self.value == other.value and 
                self.children == other.children and 
                self.props == other.props)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Validate that value is not None
        if value is None:
            raise ValueError("LeafNode must have a valid value.")
        
        
        super().__init__(tag, value, None, props)

    def to_html(self):
        
        if self.tag is None:
            return self.value  
        
        props_str = self.props_to_html()
        if props_str:
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        
        
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def props_to_html(self):
        
        if not self.props:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items()).strip()

    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # Validate that tag is not None
        if tag is None:
            raise ValueError("ParentNode must have a valid tag.")
        
        # Validate that children is not an empty list
        if not children:
            raise ValueError("ParentNode must have at least one child.")
        
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        """Renders the ParentNode as HTML"""
        if self.tag is None:
            return self.value  # Return raw text if no tag
        
        # Render properties if they exist
        props_str = self.props_to_html()
        if props_str:
            return f"<{self.tag} {props_str}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
        
        # Render the tag without properties
        return f"<{self.tag}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"

