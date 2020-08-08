# Hand-Game-Controller
Using python and OpenCV, made a game controller by detecting the hand's movement and initializing a keypress when the hand is detected in some particular region.

#Description
The screen is divided into two parts. When the hand is detected in some particular region of screen a keypress is called. But I had to maintain a list to prevent multiple keypresses at one specific instant.
Here, I have used Image segmentation to separate background and other objects. For the first 50 frames, an average of all the frames is initialized as background. Then only changes in the foreground are entertained.
