import re

def extract_markdown_images(text):
    """
    Returns a list of (alt_text, url) tuples from markdown image syntax:
    ![alt](url)
    """
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Returns a list of (anchor_text, url) tuples from markdown link syntax:
    [text](url)
    But should NOT match images (which start with !)
    """
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")