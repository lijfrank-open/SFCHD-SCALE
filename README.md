# SFCHD-SCALE
The dataset and code of the paper "[Large, Complex, and Realistic Safety Clothing and Helmet Detection: Dataset and Method](sfchd-scale.pdf)".  
Authors: Fusheng Yu†, Jiang Li†, Xiaoping Wang, Shaojin Wu, Junjie Zhang, Zhigang Zeng († Equal Contribution)  
Affiliation: Huazhong University of Science and Technology (HUST)  

## Citation
```bibtex
@article{yu2024sfchd-scale,
  title={Large, Complex, and Realistic Safety Clothing and Helmet Detection: Dataset and Method},
  author={Fusheng Yu and Jiang Li and Xiaoping Wang and Shaojin Wu and Junjie Zhang and Zhigang Zeng},
  year={2024},
  journal = {},
  volume = {},
  pages = {},
  doi={}
}
```

## Dataset Information
Comparison between SFCHD and existing open-source datasets for safety helmets
| Dataset | Year | #Category | #Sample | #Instance | Color | Task | Data Source |
|---------|------|-----------|---------|------------|-------|------|-------------|
| Pictor-v3 | 2020 | 6 | 1,330 | 9,208 | RGB | Detection | Web-mined and Crowd-sourced |
| SHWD | 2019 | 2 | 3,241 | 10,457 | RGB | Detection | Web-mined |
| SFCHD | 2023 | 7 | 12,373 | 50,558 | RGB | Detection | Chemical Plant |

Statistics of instance distribution per category in the SFCHD dataset
| Category       | Person  | Safety Helmet | Safety Clothing | Other Clothing | Head  | Blurred Clothing | Blurred Head | Total   |
|----------------|---------|---------------|-----------------|----------------|-------|-----------------|--------------|---------|
| Training       | 13,528  | 11,378        | 11,781          | 626            | 961   | 1,053           | 896         | 40,223  |
| Testing        | 3,482   | 2,920         | 3,032           | 154            | 239   | 271             | 238         | 10,336  |
| **Total**      | **17,010** | **14,298**    | **14,813**      | **780**        | **1,200** | **1,324**       | **1,134**   | **50,559** |

Category distribution of objects with different sizes in the SFCHD dataset
| Category       | Total | Large | Medium | Small |
|----------------|-------|-------|--------|-------|
| Safety Helmet  | 14,298| 3,551 | 3,030  | 7,717 |
| Head           | 1,200 | 95    | 164    | 941   |
| Blurred Clothing | 1,324 | 281   | 313    | 730   |
| Blurred Head   | 1,134 | 15    | 41     | 1,078 |

## Experimental Results
Comparisons of different methods on the Pictor-v3, SHWD, and SFCHD datasets [mAP(0.50)/mAP(0.50:0.95)]
| Method     | Backbone  | Pictor-v3 | SHWD    | SFCHD (ours) |
|------------|-----------|------------|---------|--------------|
| SSD        | VGG16     | 85.5 / 48.8 | 80.8 / 57.4 | 72.8 / 41.5  |
| Faster RCNN| ResNet-50| 90.6 / 53.4 | 84.8 / 63.1 | 76.4 / 50.3  |
| FCOS       | ResNet-50| 89.5 / 52.4 | 85.8 / 63.9 | 76.4 / 49.6  |
| VFNet      | ResNet-50| 91.4 / 55.2 | 85.7 / 63.9 | 76.4 / 51.0  |
| RetinaNet  | ResNet-50| 90.5 / 54.4 | 85.5 / 63.6 | 75.9 / 48.9  |
| TOOD       | ResNet-50| 91.5 / 55.8 | 86.7 / 64.4 | 78.9 / 52.3  |
| YOLOv5     | CSPDarknet53 | 88.2 / 53.6 | 84.0 / 63.9 | 74.1 / 49.6  |

Performance of different categories in the SFCHD dataset
| Method     | Person | Safety Helmet | Safety Clothing | Other Clothing | Head | Blurred Clothing | Blurred Head | mAP(0.50:0.95) | mAP(0.50) |
|------------|--------|----------------|-----------------|-----------------|------|-----------------|--------------|----------------|------------|
| SSD        | 60.2   | 56.5           | 55.7            | 45.2            | 38.4 | 20.5            | 14.2         | 41.5           | 72.8       |
| Faster RCNN| 71.2   | 64.7           | 64.6            | 54.5            | 49.3 | 27.2            | 20.5         | 50.3           | 76.4       |
| FCOS       | 68.4   | 63.4           | 64.6            | 54.0            | 48.0 | 28.9            | 19.6         | 49.6           | 76.4       |
| VFNet      | 73.1   | 66.2           | 64.3            | 54.0            | 52.5 | 25.1            | 22.0         | 51.0           | 76.4       |
| RetinaNet  | 71.1   | 63.5           | 64.5            | 51.8            | 48.5 | 27.1            | 15.9         | 48.9           | 75.9       |
| TOOD       | 72.9   | 66.0           | 65.9            | 56.2            | 52.8 | 29.6            | 22.3         | 52.3           | 78.9       |
| YOLOv5     | 72.7   | 66.4           | 63.7            | 54.9            | 50.7 | 21.2            | 18.9         | 49.6           | 74.1       |

Performance comparisons between our SCALE-YOLO and existing models on the ExDark dataset
| Method     | Bicycle | Boat | Bottle | Bus | Car | Cat | Chair | Cup | Dog | Motorbike | People | Table | mAP(0.50) |
|------------|---------|------|--------|-----|-----|-----|-------|-----|-----|----------|--------|-------|------------|
| YOLOv3     | 79.8    | 75.3 | 78.1   | 92.3| 83.0| 68.0 | 69.0  | 79.0 | 78.0| 77.3     | 81.5   | 55.5  | 76.4        |
| KinD       | 80.1    | 77.7 | 77.2   | 93.8| 83.9| 66.9 | 68.7  | 77.4 | 79.3| 75.3     | 80.9   | 53.8  | 76.3        |
| MBLLEN     | 82.0    | 77.3 | 76.5   | 91.3| 84.0| 67.6 | 69.1  | 77.6 | 80.4| 75.6     | 81.9   | 58.6  | 76.8        |
| Zero-DCE   | 84.1    | 77.6 | 78.3   | 93.1| 83.7| 70.3 | 69.8  | 77.6 | 77.4| 76.3     | 81.0   | 53.6  | 76.9        |
| MAET       | 83.1    | 78.5 | 75.6   | 92.9| 83.1| 73.4 | 71.3  | 79.0 | 79.8| 77.2     | 81.1   | 57.0  | 77.7        |
| DENet      | 80.4    | 79.7 | 77.9   | 91.2| 82.7| 72.8 | 69.9  | 80.1 | 77.2| 76.7     | 82.0   | 57.2  | 77.3        |
| IAT-YOLO   | 79.8    | 76.9 | 78.6   | 92.5| 83.8| 73.6 | 72.4  | 78.6 | 79.0| 79.0     | 81.1   | 57.7  | 77.8        |
| PE-YOLO    | 84.7    | 79.2 | 79.3   | 92.5| 83.9| 71.5 | 71.7  | 79.7 | 79.7| 77.3     | 81.8   | 55.3  | 78.0        |
| SCALE-YOLO | 81.3    | 79.3 | 78.2   | 93.9| 84.2| 75.5 | 74.9  | 82.3 | 81.0| 77.5     | 82.5   | 57.3  | **79.0**        |

Performance improvements of the SCALE module on the ExDark dataset
| Method       | Bicycle | Boat | Bottle | Bus | Car | Cat | Chair | Cup | Dog | Motorbike | People | Table | mAP(0.50) |
|--------------|---------|------|--------|-----|-----|-----|-------|-----|-----|----------|--------|-------|------------|
| FCOS         | 75.5    | 64.4 | 68.0   | 86.8| 78.5| 69.3 | 55.4  | 71.7 | 70.0| 64.8     | 72.3   | 46.7  | 68.6        |
| FCOS+SCALE   | 75.1    | 66.6 | 73.5   | 89.9| 78.9| 67.0 | 57.2  | 72.8 | 74.2| 67.3     | 72.0   | 45.9  | **70.0**    |
| VFNet        | 77.4    | 70.5 | 76.6   | 90.6| 81.8| 67.1 | 59.4  | 71.8 | 72.6| 70.6     | 77.7   | 53.3  | 72.5        |
| VFNet+SCALE  | 79.4    | 70.2 | 76.5   | 89.7| 81.7| 71.9 | 60.9  | 71.5 | 75.0| 71.2     | 77.4   | 55.5  | **73.4**    |
| TOOD         | 77.0    | 69.2 | 72.2   | 90.0| 80.0| 72.6 | 63.0  | 71.8 | 71.0| 71.9     | 76.2   | 52.2  | 72.3        |
| TOOD+SCALE   | 77.9    | 70.0 | 78.3   | 90.0| 80.7| 69.1 | 62.0  | 72.4 | 73.7| 69.2     | 78.1   | 54.2  | **73.0**    |

Ablation analysis for different pathways in our SCALE module
| Method             | SAP | CAP | mAP(0.50) |
|--------------------|-----|-----|-----------|
| YOLOv3             | --  | --  | 76.4      |
| SCALE-YOLO (Ours)  | ✓   | ✗   | 77.3      |
| SCALE-YOLO (Ours)  | ✗   | ✓   | 77.8      |
| SCALE-YOLO (Ours)  | ✓   | ✓   | **79.0**  |

Performance improvements of the SCALE module on the SFCHD dataset
| Method       | Person | Safety Helmet | Safety Clothing | Other Clothing | Head | Blurred Clothing | Blurred Head | mAP(0.50:0.95) | mAP(0.50) |
|--------------|--------|----------------|-----------------|-----------------|------|-----------------|--------------|----------------|------------|
| FCOS         | 68.4   | 63.4           | 64.6            | 54.0            | 48.0 | 28.9            | 19.6         | **49.6**           | **76.4**       |
| FCOS+SCALE   | 68.5   | 63.8           | 64.7            | 53.0            | 47.6 | 28.4            | 20.5         | 49.5           | 76.3       |
| VFNet        | 73.1   | 66.2           | 64.3            | 54.0            | 52.5 | 25.1            | 22.0         | 51.0           | 76.4       |
| VFNet+SCALE  | 73.2   | 66.5           | 64.4            | 53.9            | 52.1 | 25.8            | 23.7         | **51.4**           | **76.6**       |
| TOOD         | 72.9   | 66.0           | 65.9            | 56.2            | 52.8 | 29.6            | 22.3         | 52.3           | 78.9       |
| TOOD+SCALE   | 72.9   | 66.2           | 66.2            | 56.2            | 51.6 | 29.6            | 23.5         | **52.4**           | **79.3**       |
| YOLOv8       | 73.6   | 64.9           | 67.5            | 58.5            | 45.5 | 32.3            | 23.9         | 52.2           | 77.9       |
| YOLOv8+SCALE | 74.4   | 66.1           | 68.8            | 58.4            | 47.5 | 33.2            | 25.2         | **53.3**           | **78.6**       |

## Dataset Acquisition
.  
├── annotations  
├── classes.txt  
├── directory.md  
├── images  
├── labels  
├── labels.cache  
├── new_split_yolo  
├── sd_train  
├── train  
├── Vision  
└── yolo  
8 directories, 3 files

Download the dataset from [链接：https://pan.baidu.com/s/1k2pWg8r-G3KSI2Q3Tdt6kg 
提取码：v4ao], unzip and copy the files from images into dataset_SFCHD/images. Also, unzip labels.zip and yolo.zip.

Google Drive: https://drive.google.com/file/d/1-2z7r3J4sZdLvVt5mllvSEwAFO49Y-zj/view?usp=sharing