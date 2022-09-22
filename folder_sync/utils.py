import hashlib
import os

def build_path_with_diff_dir(input_path: str, input_dir_path: str, target_dir_path: str) -> str:
    """Builds path by removing input directory path from input path and adding target dir as prefix."""

    path = build_path_without_prefix(input_path, input_dir_path)
    return os.path.join(target_dir_path, path)

def build_path_without_prefix(path: str, prefix_path: str) -> str:
    """Builds path by removing the specified prefix."""

    return os.path.relpath(path, prefix_path)

def file_content_matches(file_path: str, file_path2: str):
    """Decides whether file content matches using md5 hashes."""
    
    return get_file_md5_hash(file_path) == get_file_md5_hash(file_path2)

# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def get_file_md5_hash(file_path: str) -> str:
    """
    Calculates md5 file hash reading the file chunk by chunk.

    Note: The chunk (block size) is taken as the md5 expected block size.

    Parameters
    ------------
    file_path: str
        valid path to file that exists

    Returns
    ------------
    str
        string of md5 hash as hexcode
    """
    
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(md5.block_size)
            if not chunk:
                break
            md5.update(chunk)
    return md5.hexdigest()

