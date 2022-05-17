# growingPlants
A repository to analyse images of growing plants


Use this dataset [Aberystwyth Leaf Evaluation](https://zenodo.org/record/168158#.YnjqRS8w2qB)
Which I got from [quantitative plant](https://www.quantitative-plant.org/dataset/leaf-annotation) which is a collection of datasets to do with plants.The Aberystwyth Leave

Aim is to get a measure of the "leafiness" of the images.
Start with just a simple colour-based filter.

The initial tests were done on [this timelapse youtube video](https://www.youtube.com/watch?v=MGsS91x5StQ).
Three screenshots from later in the sequence were taken of "just green". The minimum/maximum of the H channel (hsv[0]) of these was used to set the colour filters for lower_green and upper_green. This could be automated in the future or some other form of plant segmentation substituted in.


The frames of the video were extracted [to png files using ffmpeg](https://stackoverflow.com/questions/40088222/ffmpeg-convert-video-to-images)
And then any frame with green writing was removed (manually). The removed frames were:
36-218 inclusive
236-401 inclusive
418-601 inclusive
1024 - because cat
1221-1403 inclusive
1456-1638 incl
2858-3040 incl
3248-3432 incl
7578-end

calculate_green.py does the following:
- scans the source directory for files and then sorts the list of files alphabetically
- Optionally (do_crop) crops the image - these parameters will need to be customised
- converts the image to HSV
- Optionally (do_green_analysis) outputs the max, min and mean of each channel (HSV[0] means hue or colour)
- Filters for a specific colour (in our case green) and creates a mask
- Sums the mask and records it for every image in the directory
- Optionally (save_masks) saves the masked image to the destination directory
- Plots the mask values (a possible proxy for growth) on a graph

Findings: Green pixels can be used as a reasonably rough proxy for plant growth in some cases. Lighting conditions make this filtering method rough and ready (because light can change over time, weather can be different on different days).
