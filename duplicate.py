import os
import shutil
import hashlib
from collections import defaultdict

folder_path = "./images"
files = os.listdir(folder_path)
hashes = defaultdict(list)

for file in files:
    hash = hashlib.md5(open(os.path.join(folder_path, file), "rb").read()).hexdigest()
    hashes[hash].append(file)

for key, value in hashes.items():
    if len(value) > 1:
        if not os.path.exists("./duplicates"):
            os.makedirs("./duplicates")
        print(f"{key} has more than one file: {value}")
        hashes[key].pop(0)
        for file in hashes[key]:
            # os.remove(os.path.join(folder_path, file))
            shutil.move(os.path.join(folder_path, file), "./duplicates")
    else:
        print("No duplicates found.")
