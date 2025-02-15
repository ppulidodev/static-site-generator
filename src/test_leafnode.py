import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leafnode_without_tag(self):
        """Test if a LeafNode without a tag renders as raw text"""
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leafnode_with_tag(self):
        """Test if a LeafNode with a tag renders correctly"""
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_leafnode_with_props(self):
        """Test if a LeafNode with properties renders correctly"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leafnode_with_multiple_props(self):
        """Test if a LeafNode with multiple properties renders correctly"""
        node = LeafNode("a", "Click here", {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Click here</a>')

    def test_leafnode_raises_valueerror_on_empty_value(self):
        """Test if creating a LeafNode without a value raises a ValueError"""
        with self.assertRaises(ValueError):
            LeafNode("p", None)

if __name__ == "__main__":
    unittest.main()