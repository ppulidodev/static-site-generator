import unittest

from textnode import *
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_different_text(self):
        """Test if two TextNode objects with different text are not equal"""
        node1 = TextNode("Text A", TextType.BOLD)
        node2 = TextNode("Text B", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_text_type(self):
        """Test if two TextNode objects with different text types are not equal"""
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_url(self):
        """Test if two TextNode objects with different URLs are not equal"""
        node1 = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://different.com")
        self.assertNotEqual(node1, node2)

    def test_equal_with_none_url(self):
        """Test if two TextNode objects without a URL are equal"""
        node1 = TextNode("No URL", TextType.TEXT)
        node2 = TextNode("No URL", TextType.TEXT)
        self.assertEqual(node1, node2)

    def test_text_node_to_html_node_text(self):
        node1 = TextNode("Raw text", TextType.TEXT)
        node2 = text_node_to_html_node(node1)
        expected = LeafNode(None, "Raw text")
        self.assertEqual(node2, expected)

    def test_text_node_to_html_node_bold(self):
        node1 = TextNode("Bold text", TextType.BOLD)
        node2 = text_node_to_html_node(node1)
        expected = LeafNode("b", "Bold text")
        self.assertEqual(node2, expected)

    def test_text_node_to_html_node_italic(self):
        node1 = TextNode("Italic text", TextType.ITALIC)
        node2 = text_node_to_html_node(node1)
        expected = LeafNode("i", "Italic text")
        self.assertEqual(node2, expected)

    def test_text_node_to_html_node_code(self):
        node1 = TextNode("Code text", TextType.CODE)
        node2 = text_node_to_html_node(node1)
        expected = LeafNode("code", "Code text")
        self.assertEqual(node2, expected)

    def test_text_node_to_html_node_link(self):
        node1 = TextNode("Click here", TextType.LINK, url="https://example.com")
        node2 = text_node_to_html_node(node1)
        expected = LeafNode("a", "Click here", {"href": "https://example.com"})
        self.assertEqual(node2, expected)

    def test_text_node_to_html_node_img(self):
        node1 = TextNode("Image description", TextType.IMAGE, url="https://example.com/image.jpg")
        node2 = text_node_to_html_node(node1)
        expected = LeafNode("img", "", {"src": "https://example.com/image.jpg", "alt": "Image description"})
        self.assertEqual(node2, expected)


if __name__ == "__main__":
    unittest.main()