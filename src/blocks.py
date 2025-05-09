def markdown_to_blocks(markdown):
    """
    Convert markdown text to a list of blocks.
    """
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]
    return blocks
