from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node, extract_title

import os
import shutil


def copy_directory(source_directoy, destination_directory):
    
    if not os.path.lexists(source_directoy):
        
        print(f"{source_directoy}")
        raise Exception("The source directory is incorrect")
    if os.path.isdir(destination_directory):
        shutil.rmtree(f"{destination_directory}")

    os.mkdir(f"{destination_directory}")

    items = os.listdir(source_directoy)

    for item in items:
        
        new_source = os.path.join(source_directoy, item)
        new_destination = os.path.join(destination_directory, item)

        if os.path.isfile(new_source):
            shutil.copy(new_source, new_destination)
            print(f"Copying {new_source} to {new_destination}")
        else:
            copy_directory(new_source, new_destination)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()

    new_content = markdown_to_html_node(markdown_content).to_html()
    
    new_title = extract_title(markdown_content)

    new_page =  template_content.replace("{{ Title }}", new_title)
    new_page =  new_page.replace("{{ Content }}", new_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(new_page)

    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    #copy_directory(dir_path_content, dest_dir_path)
    
    
    items_in_path = os.listdir(dir_path_content)

    for item in items_in_path:
        source_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(source_path) and source_path.endswith('.md'):
            
            dest_path = os.path.join(dest_dir_path, item)
            dest_path = dest_path.replace('.md', '.html')
            generate_page(source_path, template_path, dest_path)
        
        elif os.path.isdir(source_path):
            
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(source_path, template_path, new_dest_dir)





def main():
    
    copy_directory("static", "public")

    template_path = "template.html"
    generate_pages_recursive("content", template_path, "public")

if __name__ == "__main__":
    main()