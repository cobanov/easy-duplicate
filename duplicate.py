import os
import logging
import click
import shutil
import hashlib
from collections import defaultdict

folder_path = "./json"

logging.basicConfig(
    filename="history.log", format="%(asctime)s %(message)s", filemode="a"
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def _checksum(file_path):
    absolute_path = os.path.join(folder_path, file_path)
    return hashlib.md5(open(absolute_path, "rb").read()).hexdigest()


def scan(folder_path):
    hashes = defaultdict(list)
    files = os.listdir(folder_path)
    for file in files:
        hash = _checksum(file)
        hashes[hash].append(file)
    return hashes


def fuse(hashes, remove_files=False, save_log=True):
    if not remove_files:
        if not os.path.exists("./duplicates"):
            os.makedirs("./duplicates")

    for key, value in hashes.items():
        if len(value) > 1:
            print(f"{key} has more than one file: {value}")
            hashes[key].pop(0)

            for file in hashes[key]:
                file_absolute_path = os.path.join(folder_path, file)

                if remove_files:
                    os.remove(file_absolute_path)
                    if save_log:
                        logger.info(f"{file_absolute_path} deleted succesfully.")
                else:
                    shutil.move(file_absolute_path, "./duplicates")
                    if save_log:
                        logger.info(
                            f"'{file_absolute_path}' moved to './duplicates' directory succesfully."
                        )
        else:
            print("No duplicates found.")
            if save_log:
                logger.info(
                    f"'{file_absolute_path}' moved to './duplicates' directory succesfully."
                )


def main():
    hashes = scan(folder_path)
    fuse(hashes, remove_files=False)


if __name__ == "__main__":
    main()
