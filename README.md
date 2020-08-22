# AIMS_dataset_conversion

This is for images in the frames folder only. 

NOTE: Some species are heavily biased in the original dataset. They are not normalized in this dataset.
 
1. Generate dataset JSON
```
python convert_to_json.py --reduce 100 --eval_p 15 --test_p 5 --min_ann 4 --frame_meta_csv_path "frame_metadata.csv" --middle
```
Option | Description | Example | Default
------------ | ------------- | ------------- | ------------- | 
--reduce | Percentage of dataset to use. Mainly to create smaller dataset for faster testing |--reduce 100 | 100
--eval_p | Percentage to use for evaluation |--eval_p 15 | 15
--test_p | Percentage to use for testing |--test_p 5 | 5
--min_ann | Minimum annotations an image must have before being added to the new dataset |--min_ann 4 | 4
--frame_meta_csv_path | Path to frame metadata csv |--frame_meta_csv_path "frame_metadata.csv" | "frame_metadata.csv"
--single_class | Group all species as 1 class. Useful when counting only. |--single_class | False
--middle | Convert to middle format. Setting false will leave the json in Detectron2 format |--middle | True

2. Download images in JSON. tqdm is required. Run "pip install tqdm". Will skip already downloaded files.
```
python download_dataset_from_json.py --json_path "output/middle_1324_C127_test_set.json" --base_url "https://data.pawsey.org.au/download/FDFML/frames/" --download_path "frames"
```
3. (Optional) Copy test images out of the dataset.
```
python copy_json_images_to_folder.py --json_path "output/middle_1324_C127_test_set.json" --dataset_root "frames" --destination_root "curated_dataset" --max_files 60
```
4. (Optional) Preview the dataset and annotations. 
```
python preview_annotations.py --json_path "output/middle_1324_C127_test_set.json" --dataset_root "curated_dataset" 

```