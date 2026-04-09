# YOLOv26 Upgraded: Cat-Dog Detection Pipeline

An end-to-end computer vision pipeline designed for training and deploying YOLO models on custom datasets. This repository automates the dataset acquisition from Hugging Face and handles environment configuration locally.

## 🛠 Workflow Overview

To use this repository, follow the execution order below:
1. **Download Data**: Fetch the dataset from Hugging Face.
2. **Configure Database**: Generate the `data.yaml` file with local paths.
3. **Train**: Run the training script on the prepared dataset.
4. **Predict**: Use the trained weights for inference.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/sankalpalokuliyanage/YOLOv26_upgraded.git](https://github.com/sankalpalokuliyanage/YOLOv26_upgraded.git)
cd YOLOv26_upgraded
```

## Install Requirements
```bash
pip install ultralytics huggingface_hub torch torchvision
```

## 📖 Execution Steps
Step 1: Download the Dataset
```bash
python download_data.py
```

Step 2: Configure the Database
* Run this script to generate your data.yaml. This file tells YOLO where to find the images on your specific machine.
```bash
python database_configurator.py
```

Step 3: Train the Model
```bash
python train.py
```

Step 4: Run Predictions
```bash
python predict.py
```

## L.C. Sankalpa Lokuliyanage
Kyungpook National University

