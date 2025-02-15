import unittest

from textnode import TextNode, TextType
from inline_markdown import *


class TestInlineMarkdown(unittest.TestCase):

    def test_no_delimiter(self):
        """Text without the delimiter should remain unchanged"""
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [node])

    def test_single_delimited_word(self):
        """A single delimited word should be split correctly"""
        node = TextNode("This is `code` text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_multiple_delimited_words(self):
        """Multiple delimited words should all be converted"""
        node = TextNode("This is `code` and `more code`!", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_unclosed_delimiter(self):
        """An unclosed delimiter should return unchanged"""
        node = TextNode("This is `broken code", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [node])

    def test_bold_text(self):
        """Bold text with ** should be processed correctly"""
        node = TextNode("This is **bold** text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_italic_text(self):
        """Italic text with * should be processed correctly"""
        node = TextNode("This is *italic* text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC), expected)

    def test_consecutive_delimiters(self):
        """Should handle consecutive delimiters correctly"""
        node = TextNode("This is **bold** and **strong**!", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_nested_delimiters(self):
        """Nested delimiters should not be handled here"""
        node = TextNode("This is *nested `code`*!", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("nested `code`", TextType.ITALIC),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC), expected)

    def test_single_image(self):
        """Test extracting a single image"""
        text = "This is an image ![alt text](https://example.com/image.jpg)"
        expected = [("alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        """Test extracting multiple images"""
        text = "![first](https://img1.com) and ![second](https://img2.com)"
        expected = [("first", "https://img1.com"), ("second", "https://img2.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_no_alt_text(self):
        """Test extracting an image with empty alt text"""
        text = "![](https://example.com/no-alt.jpg)"
        expected = [("", "https://example.com/no-alt.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_image(self):
        """Test when there are no images in text"""
        text = "This text has no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_malformed_image(self):
        """Test malformed image markdown does not match"""
        text = "![broken image](missing closing parenthesis"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_images_empty_text(self):
        """Test if an exception is raised for empty input"""
        with self.assertRaises(Exception):
            extract_markdown_images("")

    ## LINK EXTRACTION TESTS ##

    def test_single_link(self):
        """Test extracting a single link"""
        text = "This is a [link](https://example.com)"
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        """Test extracting multiple links"""
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_no_text(self):
        """Test extracting a link with no text"""
        text = "[](/empty-text)"
        expected = [("", "/empty-text")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        """Test when there are no links in text"""
        text = "Just normal text here."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_malformed_link(self):
        """Test malformed link markdown does not match"""
        text = "[broken link](missing closing parenthesis"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_links_empty_text(self):
        """Test if an exception is raised for empty input"""
        with self.assertRaises(Exception):
            extract_markdown_links("")

    def test_single_image(self):
        """Test splitting a single image"""
        node = TextNode("Look at this ![cat](https://img.com/cat.jpg)", TextType.TEXT)
        expected = [
            TextNode("Look at this ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://img.com/cat.jpg")
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_multiple_images(self):
        """Test splitting multiple images"""
        node = TextNode("![img1](https://1.jpg) and ![img2](https://2.jpg)", TextType.TEXT)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://1.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://2.jpg")
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_image_no_alt_text(self):
        """Test splitting an image with empty alt text"""
        node = TextNode("Image: ![](https://img.com/no-alt.jpg)", TextType.TEXT)
        expected = [
            TextNode("Image: ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://img.com/no-alt.jpg")
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_no_images(self):
        """Test when there are no images"""
        node = TextNode("Just normal text", TextType.TEXT)
        expected = [node]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_non_text_node_unchanged(self):
        """Test that non-text nodes are not changed"""
        node = TextNode("Bold text", TextType.BOLD)
        expected = [node]
        self.assertEqual(split_nodes_image([node]), expected)

    ## LINK SPLITTING TESTS ##

    def test_single_link(self):
        """Test splitting a single link"""
        node = TextNode("Check this [Google](https://google.com)", TextType.TEXT)
        expected = [
            TextNode("Check this ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com")
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_multiple_links(self):
        """Test splitting multiple links"""
        node = TextNode("[One](https://1.com) then [Two](https://2.com)", TextType.TEXT)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("One", TextType.LINK, "https://1.com"),
            TextNode(" then ", TextType.TEXT),
            TextNode("Two", TextType.LINK, "https://2.com")
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_link_no_text(self):
        """Test splitting a link with no text"""
        node = TextNode("Click here: [](/empty-link)", TextType.TEXT)
        expected = [
            TextNode("Click here: ", TextType.TEXT),
            TextNode("", TextType.LINK, "/empty-link")
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_no_links(self):
        """Test when there are no links"""
        node = TextNode("Just normal text", TextType.TEXT)
        expected = [node]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_non_text_node_unchanged(self):
        """Test that non-text nodes are not changed"""
        node = TextNode("Italic text", TextType.ITALIC)
        expected = [node]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_plain_text(self):
        text = "Hello, world!"
        expected = [TextNode("Hello, world!", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic_text(self):
        text = "This is *italic* text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_text(self):
        text = "Here is `code` example."
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" example.", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)


    def test_multiple_bold_texts(self):
        text = "**bold1** and **bold2**"
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_single_link(self):
        text = "Check this [Google](https://google.com)."
        expected = [
            TextNode("Check this ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_multiple_links(self):
        text = "[One](https://1.com) then [Two](https://2.com)"
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("One", TextType.LINK, "https://1.com"),
            TextNode(" then ", TextType.TEXT),
            TextNode("Two", TextType.LINK, "https://2.com")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_single_image(self):
        text = "Here is an image ![alt](https://image.jpg)."
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://image.jpg"),
            TextNode(".", TextType.TEXT)  # Ensure period is separate
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_multiple_images(self):
        text = "![img1](https://1.jpg) and ![img2](https://2.jpg)"
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://1.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://2.jpg")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_mixed_links_and_images(self):
        text = "Click [here](https://example.com) or see ![this](https://image.jpg)."
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" or see ", TextType.TEXT),
            TextNode("this", TextType.IMAGE, "https://image.jpg"),
            TextNode(".", TextType.TEXT)  # Ensure period is separate
        ]
        self.assertEqual(text_to_textnodes(text), expected)

   

    def test_empty_string(self):
        text = ""
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()