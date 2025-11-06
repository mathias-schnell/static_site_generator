import re
import os
import shutil
from node_helpers import markdown_to_html_node

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def copy_dir(source_dir, target_dir):
    print("Current working directory:", os.getcwd())
    
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    
    if os.path.exists(target_dir):
        print(f"Clearing destination directory: {target_dir}")
        clear_directory(target_dir)

    for root, dirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        dest_root = os.path.normpath(os.path.join(target_dir, rel_path))

        os.makedirs(dest_root, exist_ok=True)

        for filename in files:
            src_path = os.path.join(root, filename)
            dst_path = os.path.join(dest_root, filename)
            print(f"Copying {src_path} → {dst_path}")
            shutil.copy2(src_path, dst_path)

    print("✅ Copy complete!")

def extract_title(markdown):
    lines = markdown.splitlines()
    
    for line in lines:
        match = re.match(r"^#{1}\s+(.+)", line.strip())
        if match:
            return match.group(1).strip()
    
    raise ValueError("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        from_contents = f.read()
    
    with open(template_path, "r", encoding="utf-8") as f:
        template_contents = f.read()
    
    content_node = markdown_to_html_node(from_contents)
    content_title = extract_title(from_contents)

    template_contents = template_contents.replace("{{ Content }}", content_node.to_html())
    template_contents = template_contents.replace("{{ Title }}", content_title)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_contents)

def generate_pages_recursive(content_dir, template_path, dest_dir):
    for root, dirs, files in os.walk(content_dir):
        for filename in files:
            if filename.endswith(".md"):
                from_path = os.path.join(root, filename)
                relative_path = os.path.relpath(from_path, content_dir)
                dest_path = os.path.join(dest_dir, relative_path)
                dest_path = os.path.splitext(dest_path)[0] + ".html"
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(from_path, template_path, dest_path)

    print("✅ All pages generated successfully!")