# easy-duplicate
It compares the files in a folder with md5 checksums and deletes duplicate files or moves them to the desired folder.

## Requirements

```
pip install -r requirements.txt
```

## Usage
```
python duplicate.py ./path_to_folder
```
```
Usage: duplicate.py [OPTIONS] [FOLDER_PATH]

Options:
  -R, --remove BOOLEAN  remove files instead of move
  -L, --log BOOLEAN     export records of actions
  --help                Show this message and exit.
```
