import sys
import os
from gencontent import generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not basepath.endswith("/"):
        basepath += "/"

    content_dir = "./content"
    template_path = "./template.html"
    dest_dir = "./docs"

    if os.path.exists(dest_dir):
        print("Deleting docs directory...")
        os.system(f"rm -rf {dest_dir}")

    print("Copying static files to docs directory...")
    os.system(f"cp -r static/* {dest_dir}/")

    print("Generating content...")
    generate_pages_recursive(content_dir, template_path, dest_dir, basepath)

if __name__ == "__main__":
    main()
