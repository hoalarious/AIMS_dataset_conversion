import json
import os
import matplotlib.pyplot as plt
import random
dataset_root = 'dataset\\frames'
import cv2

parsed = json.load(open('train_middle_1324.json'))

for x in range(5):
    image_idx = random.randrange(0,len(parsed))
    image = parsed[image_idx]['filename']

    img_path = os.path.join(dataset_root, image)
    if not os.path.exists(img_path): continue

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    for idx, annotation in enumerate(parsed[image_idx]['ann']['bboxes']):
        x0, y0, x1, y1 = annotation
        cv2.rectangle(img, (x0,y0), (x1,y1), color=(0, 255, 0), thickness=5)
        cv2.putText(img, str(idx), (x0,y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)

    plt.imshow(img)
    plt.show()
