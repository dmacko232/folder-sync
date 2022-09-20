# TODO description and documentation

import hashlib

def delete_file(): 
    pass

def copy_file():
    pass

def create_dir(): 
    pass

def file_content_matches():
    pass

def get_file_md5_hash(file_path: str, buf_size: int=65536) -> str:
    
    md5 = hashlib.md5()
    while True:
        data = f.read(buf_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()
