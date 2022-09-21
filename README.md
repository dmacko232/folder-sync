# folder-sync

Python simple sync folder tool from scratch.

## How to use

```
python3 cli_sync.py SOURCE_PATH REPLICA_PATH LOG_PATH SECOND_INTERVAL
```
Each SECOND_INTERVAL synchronizes folder from SOURCE_PATH to folder REPLICA_PATH while logging into LOG_PATH.
- SOURCE_PATH - valid folder path, if it is file or doesn't exist then the program exits with error
- REPLICA_PATH - valid folder path, if doesn't exist then it is created
- LOG_PATH - valid log path where to output what is happening
- SECOND_INTERVAL - seconds after which to again sync, note this interval starts running after sync is done

## How it works

1. First it is checked that source folder exists and replica is created if it doesn't exist
2. Then the folders are repeatedly (each second interval) one way synced (so replica matches source)
    1. First source folder is walked top down and all the newly created directories or file changes are copied into replica while storing all traversed source paths.
    2. Secondly replica folder is walked bottom up while removing any directories/files that have not been seen in the source folder during the previous traversal.

Storing walked source directory paths when dealing with 

## Future possible improvements
- Dealing with symbolic links could be further improved upon additional specification. Currently symbolic links are treated as regular files.
- Currently, we also synchronize any metadata changes (os.stat) to directory (library filecmp is used). However this library flags the directories as changing on thhe modification time because of contents being modified. Thus, this should be resolved by ignoring directory metadata or using own stat comparison and not relying on filecmp.
- Better documentation.