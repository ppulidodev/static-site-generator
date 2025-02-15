from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes

import re



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]

    return blocks

def block_to_block_type(text):
    split_text = text.split("\n")
    if re.match(r"^#{1,6} ", text):
        return "heading"
    if text.startswith("```") and text.endswith("```"):
        return "code"
    if all(line.startswith("> ") for line in split_text):
        return "quote"
    if all(re.match(r"^[*-] ", line) for line in split_text):
        return "unorderedlist"
    
    ordered_match = [re.match(r"^(\d+)\. ", line) for line in split_text]
    if all(ordered_match) and list(map(lambda m: int(m.group(1)), ordered_match)) == list(range(1, len(split_text) + 1)):
        return "orderedlist"
    
    return "paragraph"





def markdown_to_html_node(markdown):
    sections = markdown_to_blocks(markdown)
    block_nodes = []
    
    for section in sections:
        block_type = block_to_block_type(section)

        if block_type == "heading":
            count = len(section) - len(section.lstrip('#'))
            node = LeafNode(f"h{count}", section.lstrip('# ').strip())

        elif block_type == "paragraph":
            text_nodes = text_to_textnodes(section)
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            node = ParentNode("p", html_nodes)

        elif block_type == "code":
            node = LeafNode("pre", section.strip("```"), props={"class": "code"})

        elif block_type == "quote":
            text_nodes = text_to_textnodes(section.lstrip("> ").strip())
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            node = ParentNode("blockquote", html_nodes)

        elif block_type == "unorderedlist":
            list_items = section.split("\n")
            children = []
            for item in list_items:
                text_nodes = text_to_textnodes(item[2:].strip())
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                children.append(ParentNode("li", html_nodes))
            node = ParentNode("ul", children)

        elif block_type == "orderedlist":
            list_items = section.split("\n")
            children = []
            for item in list_items:
                text_nodes = text_to_textnodes(item[item.index(".")+2:].strip())
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                children.append(ParentNode("li", html_nodes))
            node = ParentNode("ol", children)

        block_nodes.append(node)

    return ParentNode("div", block_nodes)

def extract_title(markdown):
    lines =  markdown.split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            
            return line[2:].strip()


    raise Exception("There is no heading")
        