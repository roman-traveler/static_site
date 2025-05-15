from blocks import markdown_to_html_node
from splitting_utils import extract_title


def generate_page(from_path, template_path, dest_path):
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
    print(template)
    with open(dest_path, "w") as f:
        f.write(template)