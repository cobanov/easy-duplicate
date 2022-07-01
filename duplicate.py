import os
import logging
import click
import shutil
import hashlib
from collections import defaultdict

logging.basicConfig(
    filename="history.log", format="%(asctime)s %(message)s", filemode="a"
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def _checksum(folder_path, file_path):
    absolute_path = os.path.join(folder_path, file_path)
    return hashlib.md5(open(absolute_path, "rb").read()).hexdigest()


def scan(folder_path):
    hashes = defaultdict(list)
    files = os.listdir(folder_path)
    for file in files:
        hash = _checksum(folder_path, file)
        hashes[hash].append(file)
    return hashes


def fuse(hashes, folder_path, remove_files=False, save_log=True):
    if not remove_files:
        if not os.path.exists("./duplicates"):
            os.makedirs("./duplicates")

    for key, value in hashes.items():
        if len(value) > 1:
            print(f"{key} has more than one file: {value}")
            hashes[key].pop(0)

            for file in hashes[key]:
                file_absolute_path = os.path.join(folder_path, file)
                if remove_files:  # removes file
                    os.remove(file_absolute_path)
                    if save_log:
                        logger.info(f"{file_absolute_path} deleted succesfully.")
                else:  # moves file to duplicate folder
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


@click.command()
@click.argument("folder_path", default="./")
@click.option(
    "-R",
    "--remove",
    default="False",
    type=bool,
    help="remove files instead of move",
)
@click.option(
    "-L", "--log", default="True", type=bool, help="export records of actions"
)
def main(folder_path, remove, log):
    hashes = scan(folder_path)
    fuse(hashes, folder_path, remove_files=remove, save_log=log)


if __name__ == "__main__":
    main()
