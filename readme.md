# Fish VR Project

A MS Spatial Informatics and Engineering Masters Project Umaine by Matthew Loewen
Advisory Committee

- Nicholas Giudice
- Nimesha Ranasinghe
- Max Egenhofer

Project started by Nimesha Ranasinghe & Nishad Jayasundara

## About

FishVR’s main objective is to combine artificial intelligence (AI) and virtual reality (VR) to design an interactive and adaptive system for studying fish behavior. This behavioral research is an essential part of ecology, and fish health studies. Furthermore, it aims to address gaps of research in animal behavior studies, in particular research in fish behavioral response to visual stimuli. Most existing research is either inaccurate, basic, repetitive, and/or outdated. The key difference between this project and what currently exists is that FishVR seeks to automate the process of fish tracking. The end goal for this project is to have a self-sustaining "full loop" system containing 3 different aspects of automated tracking, displaying, and recording.

[[SOMETHING ABOUT PROVIDING METRICS about tracking results]]

This goal will be completed through by the design of a two camera tracking system (See image 1). Physical setup of project requires a fishtank, 2 web cameras, an enclosure (to control light pollution and ensure uniform lighting conditions for all tests), and a diffused led strip for white light. Setup with a camera pointed directly at the front of the tank to capture x and y dimensions of of the fish tank with a camera on top to record z and y dimensions. Recordings can be combined on the y axis to confirm tracking is accurate. Once each frame of video is processed a 3D location of the fish is determined and then saved to local SQL database. Behind the fish tank a monitor is placed against the glass where visuals are displayed for the fish to interact with. These visuals are basic geometric shapes, single fish, and a school of fish, these options have parameters for a solid colored background(s) to be inserted or changed. The visuals can be manually changed via a simple GUI.

Image 1
![Image 1 - Physical setup of fishVR](./frame differencing/graphics/illustration_without_dimensions.jpg)

This tracking system will be controlled by a convolution neural network implemented through the YOLO (You Only Look Once) V3 framework. Furthermore a SORT algorithm is applied to our technique to allow for fish to be individually identified during experimentation this also accounts for tracking loss if any.

## Objectives of this project

1. A simple UI to select videos and set some settings including which visualization to show (if this takes time you can define settings at the beginning of your code, so we can change parameters directly in the code)
2. First, a user will select a pre-recorded video
3. Start the fish tracking (you already have this, use whatever the current version)
4. Start updating the database and display tracking info on a web page (I presume you already have this too - at least a basic version)
5. Visualization or the VR environment (we need to discuss this with Nishad to define what exactly we need - I am not sure we need something like Unity or a simple 2D interface)

## Completed part of the project

1. Working tracking algorithm - YOLO v3
2. SORT algorithm implemented

## To be completed

- Export tracking data to SQL database
- Visuals
- UI to control visuals
- Dual tracking
- UI for recording or live video analysis

## Why Yolo V3? and SORT

Real time low processing requirements

## Improvements to be made

### Bounding box around tank and interpolation from pixels to real world dimensions

## Challenges

### Reflections

### Sort is meant for 2D object tracking

### Multiple fish

Fish swimming too close together
