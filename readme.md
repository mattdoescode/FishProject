# Fish VR Project

An MS Spatial Informatics and Engineering Masters Project at Umaine by Matthew Loewen

Advisory Committee

- Nicholas Giudice
- Nimesha Ranasinghe
- Max Egenhofer

This project was started by Nimesha Ranasinghe & Nishad Jayasundara.

This repository and project serve as an exploration into automated experimental behavioral studies for fish. More so, this project is meant to be a guide for future research. It outlines what work has been completed and how and why to continue work on this project.

This project relies on the YOLOv3 (You Only Look Once) library to handle tracking. The library is an implementation of a deep convolutional neural network (DCNN) trained to recognize features in images. While the basics of this library are described later in this document, see the [official YOLO documentation](https://docs.ultralytics.com/) for more information. Furthermore, view the official paper of YOLOv1 [here](https://arxiv.org/abs/1506.02640) and YOLOv3 [here](https://arxiv.org/abs/1804.02767)

## About

FishVR's objective is to combine artificial intelligence (AI) and virtual reality (VR) to design an interactive and adaptive system for studying fish behavior. This behavioral research is an essential part of ecology and fish health studies. Furthermore, it aims to address research gaps in animal behavior studies, particularly behavioral responses to visual stimuli. Most existing research is either inaccurate, basic, repetitive, or outdated. The critical improvement made by this project is that FishVR seeks to automate the process of fish tracking, data collection, and experimentation. The end goal is to have an autonomous "full loop" system containing three automated tracking, recording, and displaying aspects.

These objectives are completed through the design of a two-camera tracking system (See image 1). The physical setup of the project requires a fish tank, two web cameras, an enclosure (to control light pollution and ensure uniform lighting conditions for all tests), and a diffused led strip for white light. The cameras, one pointed directly at the front of the tank to capture x and y dimensions. The other pointed at the top to record z and y dimensions. Recordings are combined on the y axis to confirm tracking is accurate. Each video frame is processed and checked for accuracy; this results in the fish's 3D location (relative to the cameras) and saved to a local SQL database. Multiple fish or a single fish can be tested at a time. However, multiple fish tracking is much more complicated (discussion on this later).

Image 1
![Image 1 - Physical setup of fishVR](https://github.com/mattdoescode/FishProject/blob/master/frame%20differencing/graphics/illustration_without_dimensions.jpg)

Behind the fish tank, a monitor is placed against the glass such that fish can see the screen. The screen will display basic geometric shapes, single simulated fish, and a school of simulated fish; these options have parameters for solid colored background(s) to be inserted or changed. The visuals can be manually adjusted via a simple GUI. These visuals are influenced based on the location of the experiment fish.

### The autonomous systems makeup, Tracking, Recording, and Displaying

#### Tracking

For tracking YOLO is used in combination with a SORT algorithm. YOLO is used for object detection and SORT is used to track objects from 1 frame to another. A note: YOLO is a very complex detection algorithm and I do not fully understand how it works. To fully understand this algorithm I would need at least another year of work and research. This being said I have achieved the full operational abilities required for this project. The research papers of YOLOv1 and YOLOv3 only offer high-level explanations of the algorithm. The following is my current level of understanding of how YOLO works.

##### YOLO

Introduced by Joseph Redmon, in his 2016 paper [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/pdf/1506.02640.pdf) a new approach to object detection capable of running in real-time is introduced. This work proposes a single neural network capable of both predicting bounding boxes and class probabilities of objects. At the time of release other object detectors are using entirely separate networks for feature extraction and object localization. This approach revolutionized real-time object detection because it achieves a high mean average projection (mAP) score (evaluation metric for object detection) double that of other real-time detectors. Improvements upon the network released in 2018 called YOLOv3, increased both the mAP score and frame per second count.

YOLO looks at object detection as a regression problem straight from pixels to bounding boxes and objects instead of a classification problem. Existing systems pass images through several networks multiple times whereas YOLO only processes an image once. Why YOLO works so well is for several reasons.1 it is able to make decisions globally about an image. 2 when training the network YOLO encodes contextual information about classes and their appearance. 3 it learns generalizable representations of objects meaning that objects in a new domain are more likely to be detected if not trained on. Finally, 4 features from the entire image are taken into account when predicting the bounding box and object. For example, YOLO is able to associate if some kind of object like a light switch is in a photo a light fixture is likely to also be somewhere in the image.

To oversimplify a bit YOLO is basically a series of convolution and pooling operations. The magic so to speak happens through the application of filters, learned training weights, and optimized activation functions. The key to YOLOs success is striking a balance between needed computational power vs strength of successful detection. Generally, the more operations applied to the CNN that is YOLO the greater the detection accuracy but at the determination of processing speed.

YOLO processes images by converting them into a S x S grid. Each grid cell predicts B bounding boxes and confidence scores for each. This confidence score is the likelihood that an object has been detected and how accurate its bounding box is. These confidence scores are defined as Confidence = Pr(Object) \* IoU. Intersection over Union or IoU; is measured as the overlap between the actual bounding box of an object and the detected bounding box of an image. This is calculated as the area of overlap divided by the area of union. Should no object be detected in a cell the confidence level is to be 0.

[[https://towardsdatascience.com/digging-deep-into-yolo-v3-a-hands-on-guide-part-1-78681f2c7e29]]

Each bounding box contains 5 values, an x position, y position, width, height, and confidence. The x and y are the center point of the object relative to the grid cell. Width and height are predicted relative to the entire image. Confidence is a collection of class probabilities defined as Pr(Classi |Object). During testing, the confidence scores from a given grid cell are multiplied by the confidence scores from each pertaining bounding box. This looks like this Pr(Classi|Object)*Pr(Object)*IoU = Pr(Classi)\*IoU. These are then saved as prediction tensors in the form of S x S x (B5 + C). According to the YOLO paper, S = 7, B = 2, and C = 20 were used when training on the Pascal VOC dataset.

This explanation is only a rough overview of how YOLO works but describes the major functions.

The YOLOv3 network architecture is a little different from the previously described YOLOv1 architecture. It has two different parts, feature extraction, and bounding box prediction. Feature extraction is done with Darknet-53 a CNN that features 52 convolutions, skip connections, and 3 prediction heads. The goal of using Darknet is to determine image features.

Feature Extractor --> Darknet53
Detection Blocks --> 53 layers

[[I DON’T HAVE A CLUE HOW THIS THING ACTUALLY WORKS OR WHAT IT DOES]]

In February 2020, Joseph Redmon publicly announced on Twitter that he is stepping away from the YOLO project. To quote him “military applications and privacy concerns eventually became impossible to ignore.” Since then YOLOv4 and YOLOv5 have been unofficially announced by Alexey Bochkovskiy a research engineer at Intel and Glenn Jocher, CEO of Ultralytics (an AI company) respectively. YOLOv4 shows roughly a 10% increase in both mAP score and performance time. YOLOv5 has no official research paper and is not fully understood.

#### Why YOLO?

In addition to being fast YOLOv3 was selected because it is able to filter out interference in the video feed. For example, while running a test in our application a virtual (non-zebra) fish will be displayed on the screen and be immediately seen through the camera. As our implementation of YOLO has no knowledge of this fish it will be ignored. Furthermore, in the case of the result of false detection, the SORT algorithm will be able to filter this out.

Furthermore, a SORT algorithm is applied to allow for fish to be individually identified during experimentation. This algorithm also accounts for tracking loss, if any.

Mean average precision (mAP) is an evaluation metric used in object detection; it is a combination of localization (location of a detected object as a bounding box) and classification (what the detected object is). This metric is used as a comparison between different network architectures and models. The mAP value is a measure of how accurate predictions are for the both bounding box and predicted item against labeled data.

To get a mAP value we first need to calculate 3 things; precision, recall, and Intersection over Union (IoU). Precision is the measure of how correct our predictions are as a percentage. This is calculated as a measure of predicted objects in an image. True positives / False positives for each image. Recall measures how well detected all true positive detections are. This is calculated as True Positive / True Positive + False Negative. IoU is measured as the overlap between the autcal bounding box of an object and the detected bounding box of an image. This is calculated as area of overlap / area of union. One final term is used IoU threshold. This is a preset value and is compared to the IoU, this will give us either a true positive or false positive detection.

With these values we can calcuate our mAP value. To grossly oversimply- the general definition for the Average Precision (AP) is finding the area under the precision-recall curve (https://towardsdatascience.com/map-mean-average-precision-might-confuse-you-5956f1bfa9e2). mAP is just taking the average of all of these.

[[NEED TO FIGURE OUT HOW MAP WORKS and WHAT MAP VALUES MEAN]]]

##### SORT

The SORT algorithm. The problem of object tracking is defined as assigning a unique ID to each detected object in consecutive frames, where the tracking method uses the output of the detection algorithm to assign those IDs. The essence of successful tracking depends on tackling the so-called association problem: Given a set measurement (i.e. object detections in a frame), which ID should be assigned to which object.

For object tracking, two state-of-the-art algorithms are SORT [m5] and DeepSORT [m6]. SORT uses a linear Kalman filter with a constant velocity model for each bounding box to predict its state (location and dimensions) in the next frame. When detection is performed in the next frame, the pairwise intersection-over-union (IOU) of the predicted bounding boxes are compared to the bounding boxes in detection results, and a cost matrix is formed. The Hungarian algorithm is then used to assign an object ID to each bounding box. Intuitively, if the
intersection of the two bounding boxes in consecutive frames is large, according to SORT, they
should correspond to the same object. Understandably, if there is a gap in object detection for
multiple frames, the IOU value when the object is detected again is very low, leading SORT to
decide that the detection must correspond to a new object. Therefore, the performance of
tracking depends to a large extent on detection performance.

DeepSORT utilizes the same idea but adds a neural network to generate features for each
detected object and uses those in addition to the predictions by the Kalman filter. However there
are two caveats,: (1) DeepSORT is pretrained on the MARS dataset, and using a custom dataset is not as streamlined as the extremely popular networks such as YOLO. (2) Compared to human pedestrians, within the same species of fish, there are no distinct visual features that allow for distinguishing between them; this is exacerbated by the low resolution of our video capture.

In short, for our application, the neural network used in DeepSORT would be practically useless
and we chose SORT instead.

#### Recording

[[Explain current code]]

[[improvements to be made -> camera calibration (grids) adjust for radial distortion, position T and orientation R]]
[[Photogrammetry]]
[[Linear transformations -> introduce parallax]]

#### Displaying

## Why YOLOv3 & What is it?

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

## What is Sort?

## Improvements to be made

### Bounding box around tank and interpolation from pixels to real-world dimensions

## Challenges

### Reflections

### Sort is meant for 2D object tracking

### Multiple fish

Fish swimming too close together

///////// NOTES

In an ideal world, your training data should closely represent your run time data as closely as possible.

When you train your own object detector, it is a good idea to leverage existing models trained on very large datasets even though the large dataset may not contain the object you are trying to detect. This process is called transfer learning.

Data augmentation is not needed.

[^https://docs.ultralytics.com/]: https://docs.ultralytics.com/
