import hashlib
import os
from typing import Iterable

def build_path_with_diff_dir(input_path: str, input_dir_path: str, target_dir_path: str) -> str:

    path = build_path_without_prefix(input_path, input_dir_path)
    return os.path.join(target_dir_path, path)

def build_path_without_prefix(path: str, prefix_path: str) -> str:

    return os.path.relpath(path, prefix_path)

def file_content_matches(file_path: str, file_path2: str):
    
    return get_file_md5_hash(file_path) == get_file_md5_hash(file_path2)

# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def get_file_md5_hash(file_path: str) -> str:
    
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(md5.block_size)
            if not chunk:
                break
            md5.update(chunk)
    return md5.hexdigest()

