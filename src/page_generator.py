from blocks import markdown_to_html_node
from splitting_utils import extract_title

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate pages from markdown files in the given directory.
    """
    import os
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, os.path.dirname(relative_path), "index.html")
                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                generate_page(from_path, template_path, dest_path, basepath)

def generate_page(from_path, template_path, dest_path,basepath="/"):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")
    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    node = markdown_to_html_node(content)
    html = node.to_html()
    print(html)
    title = extract_title(content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace("href=\"/", f"href=\"{basepath}")
    template = template.replace("src=\"/", f"src=\"{basepath}")
    print(template)
    with open(dest_path, "w") as f:
        f.write(template)

