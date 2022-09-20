# TODO add description file

from typing import Set, Optional

# TODO documentation
def sync(source_path: str, replica_path: str, logpath: str, second_interval: int):

    # if replica_path doesnt exist create
    prev_source = None
    # while True sync_folder followed by sleep second_interval
    pass

def sync_folder(source_path: str, replica_path: str, logpath: str, previously_source_paths: Optional[Set[str]]=None) -> Set[str]:

    
    # go over previously_source_paths if they not in then delete
    # 
    pass

# TODO all below into utils
def delete_file(): pass

def copy_file() pass

def create_dir pass

def file_content_matches() pass

def get_file_md5_hash() pass