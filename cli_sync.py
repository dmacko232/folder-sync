# TODO add description + README

import argparse
from fileinput import filename
import logging
import sys

from folder_sync.sync import sync


def main() -> None:
    
    parser = argparse.ArgumentParser(description="One-way sync from source folder to replica folder in given intervals")
    parser.add_argument(
        "source_path",
        type=str, 
        help="path to source folder which we sync from"
    )
    parser.add_argument(
        "replica_path",
        type=str, 
        help="path to replica folder which we sync to"
    )
    parser.add_argument(
        "log_path",
        type=str, 
        help="path to log file"
    )
    parser.add_argument(
        "second_interval",
        type=int, 
        help="second interval in which we wish to sync"
    )

    args = parser.parse_args()

    # setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(args.log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

    sync(args.source_path, args.replica_path, args.second_interval)

if __name__ == "__main__":
    main()
