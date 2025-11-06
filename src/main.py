import os
from main_helpers import clear_directory, copy_dir, generate_pages_recursive

def main():
    content_dir = "content"
    public_dir = "public"
    static_dir = "static"
    template_path = "template.html"

    clear_directory(public_dir)
    copy_dir(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir)

main()