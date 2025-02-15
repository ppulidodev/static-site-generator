import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            new_nodes.append(node)
            continue
    
        for i, part in enumerate(parts):
            if part == "":
                continue
            new_nodes.append(TextNode(part, text_type if i % 2 else TextType.TEXT))
    
    return new_nodes

def extract_markdown_images(text):
    if not text:
        raise Exception("There is no text")
    
    matches = (re.findall(r"!\[(.*?)\]\((.*?)\)", text))
    
    return matches

def extract_markdown_links(text):
    if not text:
        raise Exception("There is no text")
    
    matches = (re.findall(r"\[(.*?)\]\((.*?)\)", text))

    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if not node.text:
            new_nodes.append(node)
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = node.text
        while matches:
            alt_text, url = matches.pop(0)
            sections = text.split(f"![{alt_text}]({url})", 1)

            
            new_nodes.append(TextNode(sections[0], TextType.TEXT))

            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            
            text = sections[1] if len(sections) > 1 else ""

        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    
    for node in old_nodes:
        if not node.text:
            new_nodes.append(node)
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = node.text
        while matches:
            alt_text, url = matches.pop(0)
            sections = text.split(f"[{alt_text}]({url})", 1)

            # Capture text before the link (even if empty)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # Add the link itself
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))

            # Update remaining text for next iteration
            text = sections[1] if len(sections) > 1 else ""

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    if text == "":
        return [TextNode("", TextType.TEXT)]
    new_nodes =  [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
  
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes