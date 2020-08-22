
import json
import urllib.request
import os
from tqdm import tqdm
from pathlib import Path
import argparse

# Default command line
# python download_dataset_from_json.py --json_path "output/middle_1324_C127_test_set.json" --base_url "https://data.pawsey.org.au/download/FDFML/frames/" --download_path "frames"

###########DEFAULT_CONFIGS###########
default_json_path = "output/middle_1324_C127_test_set.json"
default_base_url = "https://data.pawsey.org.au/download/FDFML/frames/"
default_download_path = "frames"
#####################################

parser = argparse.ArgumentParser(description="copy files from json and folder")

parser.add_argument(
    "--json_path", type=str, help="Path to json", default=default_json_path
)

parser.add_argument(
    "--base_url", type=str, help="Path to images", default=default_base_url
)

parser.add_argument(
    "--download_path", type=str, help="Destination path", default=default_download_path
)

opts = parser.parse_args()
files = json.load(open(opts.json_path))

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

Path(opts.download_path).mkdir(parents=True, exist_ok=True)

for file in files:
    file_name = file['filename']
    URL = opts.base_url+file['filename']
    save_path = os.path.join(opts.download_path, file_name)
    if os.path.exists(save_path):
        print("Already got file: "+URL)
    else:
        download_url(URL, save_path)

