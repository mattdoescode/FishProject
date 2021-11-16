# Fish VR Project

An MS Spatial Informatics and Engineering Masters Project at Umaine by Matthew Loewen

Advisory Committee

- Nicholas Giudice
- Nimesha Ranasinghe
- Max Egenhofer

This project was started by Nimesha Ranasinghe & Nishad Jayasundara.

This repository and project serve as an exploration into automated experimental behavioral studies for fish. More so, this project is meant to be a guide for future research. It outlines what work has been completed and how and why to continue work on this project.

## About

FishVR's main objective is to combine artificial intelligence (AI) and virtual reality (VR) to design an interactive and adaptive system for studying fish behavior. This behavioral research is an essential part of ecology and fish health studies. Furthermore, it aims to address research gaps in animal behavior studies, particularly behavioral responses to visual stimuli. Most existing research is either inaccurate, basic, repetitive, or outdated. The critical improvement made by this project is that FishVR seeks to automate the process of fish tracking, data collection, and experimentation. The end goal is to have an autonomous "full loop" system containing three automated tracking, recording, and displaying aspects.

These objectives are completed through the design of a two-camera tracking system (See image 1). The physical setup of the project requires a fish tank, two web cameras, an enclosure (to control light pollution and ensure uniform lighting conditions for all tests), and a diffused led strip for white light. The cameras, one pointed directly at the front of the tank to capture x and y dimensions. The other pointed at the top to record z and y dimensions. Recordings are combined on the y axis to confirm tracking is accurate. Each video frame is processed and checked for accuracy; this results in the fish's 3D location (relative to the cameras) and saved to a local SQL database.

Image 1
![Image 1 - Physical setup of fishVR](https://github.com/mattdoescode/FishProject/blob/master/frame%20differencing/graphics/illustration_without_dimensions.jpg)

Behind the fish tank, a monitor is placed against the glass such that fish can see the screen. The screen will display basic geometric shapes, single simulated fish, and a school of simulated fish; these options have parameters for solid colored background(s) to be inserted or changed. The visuals can be manually adjusted via a simple GUI. These visuals are influenced based on the location of the experiment fish.

### The autonomous systems makeup, Tracking, Recording, and Displaying

#### Tracking

A convolution neural network controls this tracking system implemented through the YOLO (You Only Look Once) V3 framework.

[[Why Yolo v3, how Yolo v3 works, what exists in other applications]]

Furthermore, a SORT algorithm is applied to allow for fish to be individually identified during experimentation. This algorithm also accounts for tracking loss, if any.

#### Recording

[[Explain current code]]

[[improvements to be made -> camera calibration (grids) adjust for radial distortion, position T and orientation R]]
[[Photogrammetry]]
[[Linear transformations -> introduce parallax]]

[[Write]]

[[tracking, displaying, and recording]]

[[talk about training here]]

#### Displaying

[[See email from Nishad and write software]]

## How to train on custom data

0. Warning. Training on custom data sets can take hours to days, depending on the size of the data set and other factors.
1. Create the training data. You will need annotated images. These must be from converted videos or other images. Free online sources such as CVAT, makesense.ai, or Labelbox can help with this. My favorite resource for this is Supervise.ly.
2. Label data. This process is slightly different depending on the tool you use. Once labeled data has been acquired, it needs to be exported to fit the Yolov3 specifications.
3. Convert. From Supervise.ly, if you imported videos, convert the labeled videos to images using the "[Videos project to images project](https://app.supervise.ly/ecosystem/apps/supervisely-ecosystem%2Fturn-video-project-into-images)" plugin.
4. Download. Download the data as ".json / Images" and decompress the folder.
5. Roboflow sign up. Supervise.ly does not support exporting to Yolo, so we need to convert the data. Create a Roboflow account.
6. Upload to Roboflow. Make a new dataset on Roboflow and upload the decompressed folder from Supervise.ly. You will now see a list of all your labeled images (make sure image resizing is turned off). You can also add data augmentation here if you would like. [DATA + VAL settings?]
7. Convert again. Go to the dataset tab on Roboflow and click export -> Yolov3 Pytorch. This download will be your training data for Yolo.
8. To train Yolo, we need to create a .yaml file. This file tells Yolo where our training and validation data is, the number of classes we want (different detectable objects), and the corresponding names. A second .yaml file can be provided here to specify a network architecture change; however, the default option works for our application.
9. Training parameters. Yolo needs to be configured to process our training data correctly.
   Data: The path to the .yaml file
   Img: The size of training images (640 x 480 etc.)
   Batch: Number of parts of our dataset. The number of images used per training set. (we can't feed all our training data at once into the network).
   Epoch: Number of training rounds for the entire data set.
   Cfg: Path for the second .yaml file
   Weights: Transformation(s) to be applied to input data.
   Conf: Confidence threshold. What confidence percentage can we assume we have found the supposed object?
10. Train. This step could take hours depending on the parameters set and dataset size. Once completed, a .pt file is created.

See [here](https://github.com/ultralytics/yolov3/wiki/Train-Custom-Data) for more.

## Deliverables of this project

1. A simple UI to select videos and set some settings, including which visualization to show (if this takes time, you can define settings at the beginning of your code so that we can change parameters directly in the code)
2. First, a user will select a pre-recorded video
   Start the fish tracking (you already have this, use whatever the current version)
3. Start updating the database and display tracking info on a web page
4. Visualization or the VR environment (we need to discuss this with Nishad to define what exactly we need - I am not sure we need something like Unity or a simple 2D interface)

## Completed part of the project

1. Working tracking algorithm - YOLO v3
2. SORT algorithm implemented

## To be completed

- Export tracking data to SQL database
- Visuals
- UI to control visuals
- Dual tracking
- UI for recording or live video analysis

## Why YOLOv3

YOLOv3 is used because it's a lightweight implementation of a real-time object detection algorithm. YOLOv3 offers accelerated processing time when compared to other solutions; it is the best performing library in terms of correct predictions compared to the processing power required.

## What is Sort?

## Improvements to be made

### Bounding box around tank and interpolation from pixels to real-world dimensions

## Challenges

### Reflections

### Sort is meant for 2D object tracking

### Multiple fish

Fish swimming too close together
