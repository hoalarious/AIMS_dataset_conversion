import json
import os
from shutil import copyfile
import argparse
from pathlib import Path

# Default command line
# python convert_to_json.py json_path "output/middle_1324_C127_test_set.json" --dataset_root "frames" --destination_root "curated_dataset" --max_files 60

###########DEFAULT_CONFIGS###########
default_json_path = "output/middle_1324_C127_test_set.json"
default_dataset_root = "frames"
default_destination_root = "curated_dataset"

default_max_files = 60
#####################################

parser = argparse.ArgumentParser(description="copy files from json and folder")

parser.add_argument(
    "--json_path", type=str, help="Path to json", default=default_json_path
)

parser.add_argument(
    "--dataset_root", type=str, help="Path to images", default=default_dataset_root
)

parser.add_argument(
    "--destination_root", type=str, help="Destination path", default=default_destination_root
)

parser.add_argument(
    "--max_files", type=int, help="Max images to copy", default=default_max_files
)

opts = parser.parse_args()

files = json.load(open(opts.json_path))

total_files = len(files)
files_to_copy = min(opts.max_files, opts.max_files)

print(f'Discovered: {total_files} files in JSON. Getting {files_to_copy}.')
for i, x in enumerate(files):
    if i >= opts.max_files: break
    imageToCopy = os.path.join(opts.dataset_root, x['filename'])
    Path(opts.destination_root).mkdir(parents=True, exist_ok=True)
    # if not os.path.exists(opts.destination_root):
    #     os.makedirs(opts.destination_root)
    destinationPath = os.path.join(opts.destination_root, x['filename'])
    copyfile(imageToCopy, destinationPath)
    print(f'Copied {x["filename"]}. {i+1} of {files_to_copy} files.  \r', end="")
