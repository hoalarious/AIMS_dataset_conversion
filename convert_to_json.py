import csv
import os
import json
import random
import argparse
from pathlib import Path
from datetime import datetime

start_time = datetime.now()

# Default command line
# python convert_to_json.py --reduce 100 --eval_p 15 --test_p 5 --min_ann 4 --frame_meta_csv_path "frame_metadata.csv" --middle

###########DEFAULT_CONFIGS###########
default_reduce = 100

default_eval_p = 15
default_test_p = 5
default_min_ann = 4
default_frame_meta_csv_path = 'frame_metadata.csv'

default_single_class = False
default_middle = True
#####################################

parser = argparse.ArgumentParser(description="AIMS to dataset json")

parser.add_argument(
    "--reduce", type=int, help="Percentage of dataset to use. Mainly to create smaller dataset for faster testing", default=default_reduce
)

parser.add_argument(
    "--eval_p", type=int, help="Percentage to use for evaluation", default=default_eval_p
)

parser.add_argument(
    "--test_p", type=int, help="Percentage to use for testing", default=default_test_p
)

parser.add_argument(
    "--min_ann", type=int, help="Minimum annotations an image must have before being added to the new dataset", default=default_min_ann
)

parser.add_argument(
    "--frame_meta_csv_path", type=str, help="Path to frame metadata csv", default="frame_metadata.csv"
)

parser.add_argument("--single_class", action="store_true", help="Use only single class", default=default_single_class)

parser.add_argument("--middle", action="store_true", help="Convert to middle format", default=default_middle)

opts = parser.parse_args()

file=open(opts.frame_meta_csv_path, "r")
reader = csv.reader(file)

dataset = []

file_name_list = {}
classes = []

for idx, line in enumerate(reader):
    if idx == 0: continue
    uid, file_name, x0, y0, x1, y1, family, genus, species = line

    class_name = " ".join([family,genus,species])
    # class_name = " ".join([family])

    if class_name not in classes:
        class_id = len(classes)
        classes.append(class_name)
    else: class_id = classes.index(class_name)

    #Check if image is already added
    if not file_name in file_name_list:

        image = {
            'filename': file_name,
            'height': 1080,
            'width': 1920,
            'annotations': []
        }
        file_name_list[file_name] = len(file_name_list)
        dataset.append(image)
    else : image = dataset[file_name_list[file_name]]

    annotation = {
        'bbox': [int(x0),int(y0),int(x1),int(y1)],
        'category_id': class_id
    }
    
    image['annotations'].append(annotation)

    if not idx%10000: 
        print('Pharsed: ' + str(idx) +" rows for " + \
            str(len(dataset)) + ' images and ' + \
            str(len(classes)) + ' categories')


print('Pharsed: ' + str(idx) +" rows for " + \
    str(len(dataset)) + ' images and ' + \
    str(len(classes)) + ' classes')

#Remove images with less than minimum annotations
dataset[:] = [i for i in dataset if len(i['annotations']) >= opts.min_ann]

#make condensed class and update old class Ids
classesCondensed = []
for image in dataset:
    for annotation in image['annotations']:
        if classes[annotation['category_id']] not in classesCondensed:
            classesCondensed.append(classes[annotation['category_id']])
            newClassId = len(classesCondensed)
        else: 
            newClassId = classesCondensed.index(classes[annotation['category_id']])

        #Single class option
        if opts.single_class:
            annotation['category_id'] = 0
        else: 
            annotation['category_id'] = newClassId

#Single class option. Override.
if opts.single_class:
    classesCondensed = ["FISH"]

#Split data into train, eval, test
#Get test data
train_json = []
test_json = []
eval_json = []

dataset[:] = dataset[:int(len(dataset)*opts.reduce/100)]

##If converting to middle format
if opts.middle:
    for image in dataset:
        middle_ann = {
            'bboxes': [],
            'labels': []
        }
        for idx, annotation in enumerate(image['annotations']):
            middle_ann['bboxes'].append(annotation['bbox'])
            middle_ann['labels'].append(annotation['category_id'])
        image['ann'] = middle_ann
        del image['annotations']

random.seed(0)
total_images = len(dataset)
ids_to_get = total_images*opts.eval_p/100
while(len(eval_json) < ids_to_get):
    indexToMove = random.randrange(0,len(dataset))
    eval_json.insert(0, dataset.pop(indexToMove))

ids_to_get = total_images*opts.test_p/100
while(len(test_json) < ids_to_get):
    indexToMove = random.randrange(0,len(dataset))
    test_json.insert(0, dataset.pop(indexToMove))

train_json = dataset

print("Train images: " + str(len(train_json)))
print("Eval images: " + str(len(eval_json)))
print("Test images: " + str(len(test_json)))
print("Classes: " + str(len(classesCondensed)))

classes_file = '';
for c in classesCondensed:
    classes_file = classes_file + c + '\n'

classesCount = len(classesCondensed)

imagesCount = str(len(train_json))

if opts.middle:
    dataset_format = "middle"
else:
    dataset_format = "detectron2"

Path("output").mkdir(parents=True, exist_ok=True)

with open(F'output/{dataset_format}_{imagesCount}_C{classesCount}_train_set.json', 'w') as f:
    json.dump(train_json, f)
with open(F'output/{dataset_format}_{imagesCount}_C{classesCount}_eval_set.json', 'w') as f:
    json.dump(eval_json, f)
with open(F'output/{dataset_format}_{imagesCount}_C{classesCount}_test_set.json', 'w') as f:
    json.dump(test_json, f)

file1 = open(f"output/classes{classesCount}.txt","w") 
file1.writelines(classes_file) 
file1.close()

current_time = start_time.strftime("%H:%M:%S")
print("Process began at: ", current_time)
end_time = datetime.now()
current_time = end_time.strftime("%H:%M:%S")
print("Process finished at: ", current_time)
time_taken = end_time - start_time
print("Process took: ", time_taken)