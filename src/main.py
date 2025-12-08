import os
import shutil
import sys
from markdown_to_html import markdown_to_html_node
from extract import extract_title

def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)

        if os.path.isdir(src_item):
            copy_directory(src_item, dst_item)
        else:
            shutil.copy(src_item, dst_item)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template_html = f.read()

    content_node = markdown_to_html_node(markdown)
    content_html = content_node.to_html()

    title = extract_title(markdown)

    full_html = template_html.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", content_html)

    # REQUIRED BY ASSIGNMENT
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)

    print(f"Wrote page to {dest_path}")

def generate_pages_recursive(content_dir, template_path, docs_dir, basepath):
    for root, dirs, files in os.walk(content_dir):
        for filename in files:
            if filename.endswith(".md"):
                content_path = os.path.join(root, filename)
                relative_path = os.path.relpath(content_path, content_dir)
                parts = relative_path.split(os.sep)

                # Determine destination directory
                if parts[-1] == "index.md":
                    dest_dir = os.path.join(docs_dir, *parts[:-1])  # all but filename
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, "index.html")
                else:
                    dest_dir = os.path.join(docs_dir, *parts)
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, "index.html")

                generate_page(content_path, template_path, dest_path, basepath)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    docs_dir = "docs"
    static_dir = "static"
    content_dir = "content"
    template_path = "template.html"

    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)

    shutil.copytree(static_dir, docs_dir)

    generate_pages_recursive(
        content_dir,
        template_path,
        docs_dir,
        basepath
    )

    print("Site generation complete.")

if __name__ == "__main__":
    main()