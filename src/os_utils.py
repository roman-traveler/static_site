
def copy_src_dir_to_dst_dir(src_dir, dst_dir):
    """
    Copy the contents of src_dir to dst_dir.
    """
    import os
    import shutil

    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Source directory {src_dir} does not exist.")
    shutil.rmtree(dst_dir, ignore_errors=True)
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dst_item = os.path.join(dst_dir, item)
        if os.path.isdir(src_item):
            shutil.copytree(src_item, dst_item)
        else:
            shutil.copy(src_item, dst_item)