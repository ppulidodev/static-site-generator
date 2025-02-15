import unittest
from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):

    def test_parentnode_renders_correctly(self):
        """Test if ParentNode renders correct nested HTML"""
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><p>First paragraph</p><p>Second paragraph</p></div>")

    def test_parentnode_without_tag_raises_error(self):
        """Test if ParentNode raises error when tag is missing"""
        child = LeafNode("p", "Some text")
        with self.assertRaises(ValueError):
            ParentNode(None, [child])

    def test_parentnode_without_children_raises_error(self):
        """Test if ParentNode raises error when no children are provided"""
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_parentnode_with_attributes(self):
        """Test if ParentNode renders attributes correctly"""
        child = LeafNode("p", "Hello")
        parent = ParentNode("section", [child], {"class": "container"})
        self.assertEqual(parent.to_html(), '<section class="container"><p>Hello</p></section>')

if __name__ == "__main__":
    unittest.main()
