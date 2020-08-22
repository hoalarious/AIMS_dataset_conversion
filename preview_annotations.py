import json
import os
import matplotlib.pyplot as plt
import random
dataset_root = 'test_frames'
import cv2
import argparse
from pathlib import Path

# Default command line
# python preview_annotations.py --json_path "output/middle_1324_C127_test_set.json" --dataset_root "curated_dataset" 

###########DEFAULT_CONFIGS###########
default_json_path = "output/middle_1324_C127_test_set.json"
default_dataset_root = "curated_dataset"
#####################################

parser = argparse.ArgumentParser(description="copy files from json and folder")

parser.add_argument(
    "--json_path", type=str, help="Path to json", default=default_json_path
)

parser.add_argument(
    "--dataset_root", type=str, help="Path to images", default=default_dataset_root
)

opts = parser.parse_args()


parsed = json.load(open(opts.json_path))

for x in range(5):
    image_idx = random.randrange(0,len(parsed))
    image = parsed[image_idx]['filename']

    img_path = os.path.join(opts.dataset_root, image)
    if not os.path.exists(img_path): continue

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    for idx, annotation in enumerate(parsed[image_idx]['ann']['bboxes']):
        x0, y0, x1, y1 = annotation
        cv2.rectangle(img, (x0,y0), (x1,y1), color=(0, 255, 0), thickness=5)
        cv2.putText(img, str(idx), (x0,y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)

    plt.imshow(img)
    plt.show()
