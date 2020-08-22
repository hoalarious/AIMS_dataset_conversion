# AIMS_dataset_conversion
 
1. Generate dataset JSON
```
python convert_to_json.py --reduce 100 --eval_p 15 --test_p 5 --min_ann 4 --frame_meta_csv_path "frame_metadata.csv" --middle
```
Option | Description | Example | Default
------------ | -------------
--reduce | Content from cell 2 |--reduce 100 | 100
--eval_p | Content in the second column |--eval_p 15 | 15
--test_p | Content in the second column |--test_p 5 | 5
--min_ann | Content in the second column |--min_ann 4 | 4
--frame_meta_csv_path | Content in the second column |--frame_meta_csv_path "frame_metadata.csv" | "frame_metadata.csv"
--middle | Content in the second column |--middle | False


2. Download images in JSON
```
python download_dataset_from_json.py --json_path "output/middle_1324_C127_test_set.json" --base_url "https://data.pawsey.org.au/download/FDFML/frames/" --download_path "frames"
```
3. Preview the dataset and annotations
```
python convert_to_json.py json_path "output/middle_1324_C127_test_set.json" --dataset_root "frames" --destination_root "curated_dataset" --max_files 60
```
4. (Optional) Copy test images out of the dataset.
```
python convert_to_json.py json_path "output/middle_1324_C127_test_set.json" --dataset_root "frames" --destination_root "curated_dataset" --max_files 60
```
