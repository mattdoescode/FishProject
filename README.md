# FishProject
Project studying Zebrafish and their movement dependent on external factors

### Project Members 
- Dr. Nimesha Ranasinghe https://umaine.edu/scis/people/nimesha-ranasinghe/
- Dr. Nishad Jayasundara https://umaine.edu/marine/faculty/nishad-jayasundara/
- Matthew Loewen 

### File Structure
*fishVR/
  *code dr.Nimesha wrote. Maps a users face to simulate a fishmovement 
*main-project/
  *dual-camera.py -> track fish movement in a 3D space. Record tracking to CSV positions
  *single-camera.py -> same as above but in a 2D space. 
  *videoRecorder.py -> records video from 2 cameras
  *visualize.py -> reads from a csv to simulate a fish movement 
*multi-object-tracking/
  *example project on frame differencing + tracking
*openCV_eamples/
  *examples from CSV on tracking
*unique-object-tracking/
  *example on unique object tracking -> can probably delete code
*functions.py -> main functions used by all sketches
