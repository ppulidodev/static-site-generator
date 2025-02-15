import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestMarkdownToBlocks(unittest.TestCase):

    def test_single_heading(self):
        markdown = "# This is a heading"
        expected = ["# This is a heading"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_paragraph(self):
        markdown = "This is a paragraph with **bold** and *italic* text."
        expected = ["This is a paragraph with **bold** and *italic* text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_list_items(self):
        markdown = "* Item 1\n* Item 2\n* Item 3"
        expected = ["* Item 1\n* Item 2\n* Item 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_blocks(self):
        markdown = """# Heading

This is a paragraph.

* List item 1
* List item 2
* List item 3"""

        expected = [
            "# Heading",
            "This is a paragraph.",
            "* List item 1\n* List item 2\n* List item 3"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)


    def test_only_newlines(self):
        markdown = "\n\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    # Headings
    assert block_to_block_type("# Heading") == "heading"
    assert block_to_block_type("## Subheading") == "heading"
    assert block_to_block_type("###### Smallest Heading") == "heading"
    assert block_to_block_type("####### Too many hashes") == "paragraph"  # More than 6 `#` should be a paragraph

    # Code Blocks
    assert block_to_block_type("```\nCode inside block\n```") == "code"
    assert block_to_block_type("```python\nprint('Hello!')\n```") == "code"
    assert block_to_block_type("`` No triple backticks") == "paragraph"  # Not a proper code block

    # Blockquotes
    assert block_to_block_type("> This is a quote") == "quote"
    assert block_to_block_type("> Line 1\n> Line 2") == "quote"
    assert block_to_block_type("This is not > a quote") == "paragraph"  # The `>` must be at the start

    # Unordered Lists
    assert block_to_block_type("* Item 1\n* Item 2\n* Item 3") == "unorderedlist"
    assert block_to_block_type("- Item 1\n- Item 2") == "unorderedlist"
    assert block_to_block_type("*Valid\n-But mixed") == "paragraph"  # Mixing `*` and `-` is invalid
    assert block_to_block_type("*No space") == "paragraph"  # Needs space after `*`

    # Ordered Lists
    assert block_to_block_type("1. First item\n2. Second item\n3. Third item") == "orderedlist"
    assert block_to_block_type("1. First item\n3. Wrong order") == "paragraph"  # List must be sequential
    assert block_to_block_type("1.First item") == "paragraph"  # Needs space after `.`
    assert block_to_block_type("1. Item\n2. Item\n4. Skipped number") == "paragraph"  # Should be sequential

    # Paragraphs (Default Case)
    assert block_to_block_type("This is a normal paragraph.") == "paragraph"
    assert block_to_block_type("**Bold text but not a block**") == "paragraph"
    assert block_to_block_type("1) Not a list format") == "paragraph"

def test_markdown_to_html_node():
    markdown = """# Heading 1
    
    Paragraph text with **bold** and *italic*.

    ```
    Code block
    ```

    > Quote text

    * Item 1
    * Item 2

    1. First item
    2. Second item
    """

    node = markdown_to_html_node(markdown)

    assert node.tag == "div"
    assert len(node.children) == 6  # 6 blocks
    
    assert isinstance(node.children[0], LeafNode)
    assert node.children[0].tag == "h1"
    
    assert isinstance(node.children[1], ParentNode)
    assert node.children[1].tag == "p"
    
    assert isinstance(node.children[2], LeafNode)
    assert node.children[2].tag == "pre"
    
    assert isinstance(node.children[3], ParentNode)
    assert node.children[3].tag == "blockquote"

    assert isinstance(node.children[4], ParentNode)
    assert node.children[4].tag == "ul"
    assert len(node.children[4].children) == 2
    assert node.children[4].children[0].tag == "li"

    assert isinstance(node.children[5], ParentNode)
    assert node.children[5].tag == "ol"
    assert len(node.children[5].children) == 2
    assert node.children[5].children[0].tag == "li"

    assert node.children[1].children[1].tag == "strong"  # Bold check
    assert node.children[1].children[3].tag == "em"  # Italic check

class TestMarkdownTitleExtractor(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Simple Title\nContent here"
        self.assertEqual(extract_title(markdown), "Simple Title")

    def test_no_title(self):
        markdown = "Just some content\nNo title here"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "There is no heading")

    def test_multiple_titles(self):
        markdown = "# First Title\n## Second Level\n# Another Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_empty_string(self):
        with self.assertRaises(Exception) as context:
            extract_title("")
        self.assertEqual(str(context.exception), "There is no heading")

    def test_title_with_special_characters(self):
        markdown = "# Title with #, ## and ### symbols"
        self.assertEqual(extract_title(markdown), "Title with #, ## and ### symbols")

    def test_title_with_multiple_spaces(self):
        markdown = "#    Title    with    spaces    \nContent"
        self.assertEqual(extract_title(markdown), "Title    with    spaces")

    def test_title_after_content(self):
        markdown = "Some content\n# Title\nMore content"
        self.assertEqual(extract_title(markdown), "Title")

    def test_multiline_title(self):
        markdown = "# Title that\ncontinues on next line"
        self.assertEqual(extract_title(markdown), "Title that")

    def test_title_with_markdown_formatting(self):
        markdown = "# Title with *italic* and **bold**"
        self.assertEqual(extract_title(markdown), "Title with *italic* and **bold**")


if __name__ == '__main__':
    unittest.main()





