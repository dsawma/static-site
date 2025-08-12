import pathlib
import shutil
from textnode import TextNode, TextType
import os
import sys
from block import extract_title, markdown_to_html_node

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

def copy_static(src, dest):
    #if dest(public) doesn't exist, make it 
    if not os.path.exists(dest):
        os.mkdir(dest)

    # list out all items in src subdirectory 
    for filename in os.listdir(src):
        from_path = os.path.join(src, filename)
        dest_path = os.path.join(dest, filename)
        #copies the path from to dest of that item
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_static(from_path, dest_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f1, open(template_path, 'r') as f2:
        rf1 = f1.read()
        rf2 = f2.read()
        content = markdown_to_html_node(rf1).to_html()
        title = extract_title(rf1)
        rf2 = rf2.replace("{{ Title }}", title).replace("{{ Content }}", content)
        rf2 = rf2.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, 'w') as f3:
        f3.write(rf2)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath, root =None):
    if root is None:
        root = dir_path_content
    for filename in os.listdir(dir_path_content):
        full_path = pathlib.Path(os.path.join(dir_path_content, filename))
        relative_path = full_path.relative_to(pathlib.Path(root))
        dest = pathlib.Path(os.path.join(dest_dir_path,relative_path ))
        if os.path.isfile(full_path):
            if full_path.suffix == ".md":
                
                dest = dest.with_suffix(".html")
                if not os.path.exists(dest.parent):
                    os.makedirs(dest.parent, exist_ok=True)
                generate_page(str(full_path), template_path, str(dest), basepath)
    
        else:
            generate_pages_recursive(str(full_path), template_path, dest_dir_path, basepath, root)



main()