This is an example pipeline on how to convert output from Blender Randomiser to COCO format labelling in preperation of fine tuning polyps detection using YOLOv7

# Data Preperation
Once the segmentation of polyps are obtained. Use find_bounding_box.ipynb to output the bounding box information as text files.

show_bbox.ipynb can be used to show if the correct bounding boxes have been converted.

# IMPORTANT!
**<span style="color:red">
When Google Colab session finishes, ALL data is wiped, please save the models!
</span>**
## To tune the model using custom data:
- clone yolov7 git and install it https://github.com/WongKinYiu/yolov7; pip install -r requirements.txt
- log into wandb account (your own API - see below) DO NOT SHARE!
- run python training script

```python train.py --epochs 100 --device 0 --entity colon_coders --workers 8 --batch-size 32 --data /content/colon.yaml --img 512 512 --cfg /content/yolov7_training_config.yaml --weights '/content/yolov7_training.pt' --name yolov7-colon --hyp data/hyp.scratch.custom.yaml```

## Google colab instructions
- upload polyps.zip to google drive
- upload colon.yaml, yolov7_training.pt, yolov7_training_config.yaml to google drive
- open google colab and mount drive
- unzip polyps.zip
```python
import zipfile
with zipfile.ZipFile("/content/drive/MyDrive/polyps.zip", 'r') as zip_ref:
    zip_ref.extractall("/content/colon_data")
```
- Important: remove the cache files (otherwise the model will use the cache file to load the data which has the incorrect file paths)
- could use to code in show_bbox.ipynb to see if data and bounding boxes has been loaded correctly
- install yolo7
```python
!git clone https://github.com/WongKinYiu/yolov7
%cd yolov7
!pip install -r requirements.txt
```
- set up wandb
```python
!pip install wandb
import wandb
wandb.login()
```
- tune model: make sure colon.yaml has the correct file paths for data, also make sure --data, --cfg and --weights has the correct file paths

```python train.py --epochs 100 --device 0 --entity colon_coders --workers 8 --batch-size 32 --data /content/colon.yaml --img 512 512 --cfg /content/yolov7_training_config.yaml --weights '/content/yolov7_training.pt' --name yolov7-colon --hyp data/hyp.scratch.custom.yaml```
- When training is finished, model output is saved under yolov7/runs/train

## Run on test data
!python test.py --data /content/colon.yaml --img 512 --batch 32 --conf 0.001 --iou 0.65 --device 0 --weights runs/train/yolov7-colon2/weights/best.pt --name yolov7_colon_val

## Notes
- The data location is specified in the config file colon.yaml
- Training config is specified in yolov7_training_config.yaml

## Weights and Biases
Weights and Biases is a very good tool to use to track training progress. YoloV7 uses this tool and it is very easy to set up
- https://wandb.ai/site/research sign up for the free account
- log into your account, go to top right, under your name select "user profile"
- go to section "danger zone" and reveal your API code
- this code is then used to log in to wandb when prompted
- when you finish you can change the API or throw it away.
- when training is in progress, go to WandB website, click on top left, you should see the project YOLO which will show the current training session
