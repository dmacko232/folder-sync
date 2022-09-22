from typing import Set, List, Callable
import time
import os
import logging

from folder_sync.utils import build_path_with_diff_dir
from folder_sync.copy import copy_dir_without_content, copy_file

def sync(source_path: str, replica_path: str, second_interval: int) -> bool:
    """
    Synchronizes folder from source path to the replica path each specified second.

    Note: if folder in replica path doesnt exist then creates one.

    Parameters
    ------------
    source_path: str
        valid path to source dir
    replica_path: str
        valid path to where copy the source dir
    second_interval: int
        interval in seconds when to sync

    Returns
    ------------
    bool
        in case of failure return False
    """

    if not os.path.exists(source_path):
        logging.error("Source directory doesnt exist.")
        return False
    if not os.path.isdir(source_path):
        logging.error("Source file exists but is not directory.")
        return False
    os.makedirs(replica_path, exist_ok=True) # create replica path dir just in case
    counter = 1
    while True:
        logging.info(f"Syncing folder {counter} time.")
        sync_folder(source_path, replica_path)
        time.sleep(second_interval)
        counter += 1


def sync_folder(source_dir_path: str, replica_dir_path: str) -> None:
    """
    Performs folder sync from source to replica.

    Note: both folders must exist!

    Parameters
    ------------
    source_dir_path: str
        valid path to source dir
    replica_dir_path: str
        valid path to where copy the source dir
    """

    # first copy changes and store the paths traversed in source_dir_path
    source_paths = _sync_folder_copy_changes(source_dir_path, replica_dir_path)
    # second delete 
    _sync_folder_delete_changes(source_dir_path, set(source_paths), replica_dir_path)
        
def _sync_folder_copy_changes(source_dir_path: str, replica_dir_path: str) -> List[str]:
    """
    Performs folder sync of copy changes from source to replica.

    Note: copy changes means new files/dirs and content changes are propagated from source to replica.

    Parameters
    ------------
    source_dir_path: str
        valid path to source dir
    replica_dir_path: str
        valid path to where copy the source dir

    Returns
    ------------
    List[str]
        list of all walked source paths
    """

    def _copy(root: str, name: str, copy_func: Callable[[str, str], None], out_paths: List[str]) -> None:
        try:
            source_path = os.path.join(root, name)
            out_paths.append(source_path)
            replica_path = build_path_with_diff_dir(source_path, source_dir_path, replica_dir_path)
            copy_func(source_path, replica_path)
        except Exception as e:
            logging.error("Exception during copying file: " + str(e))

    walked_source_paths = []
    for root, dirs, fnames in os.walk(source_dir_path, topdown=True):
        for fname in fnames:
            _copy(root, fname, copy_file, walked_source_paths)
        for dir in dirs:
            _copy(root, dir, copy_dir_without_content, walked_source_paths)
    return walked_source_paths

def _sync_folder_delete_changes(source_dir_path: str, source_paths: Set[str], replica_dir_path: str) -> None:
    """
    Performs folder sync of delete changes from source to replica.

    Note: During this method the replica dir is walked bottom up
    Note: Source paths are taken as precomputed argument so we dont have to walk the source two times

    Parameters
    ------------
    source_dir_path: str
        valid path to source dir
    source_paths: Set[str]
        set of all source paths in the previous walk of source dir
    replica_dir_path: str
        valid path to where copy the source dir

    Returns
    ------------
    List[str]
        list of all walked source paths
    """

    def _remove(root: str, name: str, remove_func: Callable) -> None:
        try:
            replica_path = os.path.join(root, name)
            source_path = build_path_with_diff_dir(replica_path, replica_dir_path, source_dir_path)
            if source_path not in source_paths: # we havent seen the path
                logging.info(f"REMOVE: {replica_path}.")
                remove_func(replica_path)
        except Exception as e:
            logging.error("Exception during removing file: " + str(e))

    for root, dirs, fnames in os.walk(replica_dir_path, topdown=False):
        for fname in fnames:
            _remove(root, fname, os.remove)
        for dir in dirs:
            _remove(root, dir, os.rmdir)

