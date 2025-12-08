import os
import shutil
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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template_html = f.read()

    # Convert markdown ? HTML
    content_node = markdown_to_html_node(markdown)
    content_html = content_node.to_html()

    # Extract title
    title = extract_title(markdown)

    # Fill the template
    full_html = template_html.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", content_html)

    # Make sure the dest directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)

    print(f"Wrote page to {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            content_path = os.path.join(root, filename)
            relative = os.path.relpath(content_path, dir_path_content)

            if filename == "index.md":
                # write to the directory URL
                dest_dir = os.path.join(
                    dest_dir_path,
                    os.path.dirname(relative),
                )
            else:
                # non-index markdown files (future proofing)
                name = os.path.splitext(filename)[0]
                dest_dir = os.path.join(
                    dest_dir_path,
                    os.path.dirname(relative),
                    name,
                )

            dest_path = os.path.join(dest_dir, "index.html")
            generate_page(content_path, template_path, dest_path)

def main():
    # Clean + rebuild public directory
    public_dir = "public"
    static_dir = "static"
    content_dir = "content"
    template_path = "template.html"

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    shutil.copytree(static_dir, public_dir)

    # Generate ALL pages
    generate_pages_recursive(content_dir, template_path, public_dir)

    print("Site generation complete.")

if __name__ == "__main__":
    main()