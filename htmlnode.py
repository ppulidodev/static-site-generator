

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
    

class LeafNode():
    def __init__(self, tag, value, props):
        if value is None:
            raise ValueError("This value cannot be None!")
        super().__init__(self,tag, value, props)


    def to_html(self):
        if self.value is None:
            raise ValueError("This value cannot be None!")
        if self.tag is None:
            return f"{self.value}"
        
        
        return f"<{self.tag} > {self.value} </{self.tag}>"
