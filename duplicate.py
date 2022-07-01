import os
import click
import shutil
import hashlib
from collections import defaultdict

folder_path = "./images"


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


def fuse(hashes, remove_files=False):
    if not remove_files:
        if not os.path.exists("./duplicates"):
            os.makedirs("./duplicates")

    for key, value in hashes.items():
        if len(value) > 1:
            print(f"{key} has more than one file: {value}")
            hashes[key].pop(0)
            for file in hashes[key]:
                if remove_files:
                    os.remove(os.path.join(folder_path, file))
                else:
                    shutil.move(os.path.join(folder_path, file), "./duplicates")
        else:
            print("No duplicates found.")


def main():
    hashes = scan(folder_path)
    fuse(hashes, remove_files=False)


if __name__ == "__main__":
    main()
