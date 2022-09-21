import os
import filecmp
import shutil
import logging

from folder_sync.utils import file_content_matches

def copy_dir_without_content(source_path: str, target_path: str) -> None:

    if not os.path.isdir(target_path): # either not dir or doesnt exist
        if os.path.exists(target_path): # exists as file
            os.remove(target_path)
            logging.info(f"REMOVE: file {target_path} because it should be dir")
        # now there is nothing in target path => we make dir and copy stat
        os.mkdir(target_path)
        logging.info(f"CREATE: dir {target_path}")
        shutil.copystat(source_path, target_path)
        logging.info(f"COPY: dir metadata from {source_path} to {target_path}")
    elif not filecmp.cmp(source_path, target_path, shallow=True): # dir exists but stat is not matching
        shutil.copystat(source_path, target_path)
        logging.info(f"COPY: dir metadata from {source_path} to {target_path}")

def copy_file(source_path: str, target_path: str) -> None:

    if not os.path.isfile(target_path): # either not file or doesnt exist
        if os.path.exists(target_path): # exists as dir
            os.rmdir(target_path)
            logging.info(f"REMOVE: dir {target_path} because it should be file")
        # we copy content and both stat
        shutil.copy2(source_path, target_path, follow_symlinks=False)
        logging.info(f"CREATE: file {target_path}")
        logging.info(f"COPY: file content from {source_path} to {target_path}")
    # if stat is different or file content doesnt match, we copy
    # NOTE: shutil doesnt use hashing, thus we use our own file content match with hash
    elif not filecmp.cmp(source_path, target_path, shallow=True) or not file_content_matches(source_path, target_path):
        logging.info(f"COPY: file content from {source_path} to {target_path}")
        shutil.copy2(source_path, target_path, follow_symlinks=False)
    # NOTE: we could just check file content first and if its matching then check the stat of file
    # and in case file content matches but stat does not just copy stat using shutil.copystat()
    # however, I believe we can just for simplicity copy whole file in case stat differs
    # this also saves us one possible file sequence scan in case

