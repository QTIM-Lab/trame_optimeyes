
## Center:
- The image after all is most important.
- Goes without saying probably to maintain aspect ratio. and fill other space as black.
- We will likely have tasks with batches of images and so a small status bar across the top (black with white text) to help the user navigate and know where they are at would be helpful. They will also have the left side bar as an additional navigation and preview.

## Left side (collapsable):
- We long term plan to server batches of images and so want to be able to see a preview of the image and any annotations already made to it
- Questions around saving batches of annotations and or 1 annotation at a time. Maybe any updates are always continuously written to db. Anyways, if that is my role  that is fine but wanted to give you an idea of the use case anyway.

## Right side (collapsable):
- Annotations
- I'm not 100% sure of the toggle between mask and polygon mode (on\off button looking switch in the top right)
- I broke into two groups originally (mask\polygon) and was intending to indicate that with the "mask\polygon" toggle button on the right. Still not sure if we need the distinction. An annotation could have both of these annotation types or one of each. Might be best to just list all annotation types you have in the entirety of the right bar real estate.

## Top:
- Zoom and Pan (I forgot to add a pan icon but even if just using the mouse moves the image intuitively while zoomed, that is fine and less clutter is a theme we want anyways).
- Ruler: Not huge but if we had some metadata for an image such as mm/px maybe this is doable. Not the priority.
- Was thinking if you select brush or eraser, you enter mask mode automatically
	- MonaiLabel pieces: Not sure how much is being done by you all so no pressure but I was thinking we generally have brush\masks in different colors with names for annotations.
		- For Monai models you would simply define a rectangular ROI and send that into a specified model for inference and have it return a mask that can be pasted onto the image in the same ROI.
		- Option to use whole image by default as ROI.
- If you select polygon, footprint, or edge tracer, you enter polygon mode automatically:
	- polygon: As basic as it sounds, with ability to move any point retroactively
		- Probably want to be able to name them and or delete them
	- footprint: A pencil like tool that allows the user to draw curves and drop polygon points at a specified spatial interval (px). Should auto close polygon after 3 points or there should be a way to ensure user knows we need a polygon, not a line.
	- edge tracer: Not sure if possible for you all or what the tooling is like but this would somehow auto detect large intensity gradients (or use a different edge detection method) and create a border guess. I have heard of drawing a collapsable lasso or rough polygon\amoeba around something and it collapses to some detected edge. I've also heard of using a "wide paint brush" to capture an edge ROI (thick outline) and then detecting the edge from within that boundary. It would be ideal if the edges were still editable and or if polygon dots along edge are automatically dropped or if we could drop them with a similar setting like pixel or mm spatial intervals along line.
	- Stretch goal: For all polygons would be nice to be able to have an option that allows users to capture the enclosed area and generate a mask segmentation from it and paste onto a preexisting brush/mask annotation or create a new brush/mask annotation from poylgon. 
- The black, green and red segmentations on the right weren't meant to all be shown at once (or maybe so, still deciding). I figured whichever tool you select in the polygon realm shows those annotations, but I keep going back and forth on just showing them all.
	- For saving all polygon type annotations, I figured we could store the same data structure where basically we use a coco style format to capture information (I use one already in my other app if you want an example). 
	- Even though the way the app allows the user to interact to create a polygon seg might be different, the result should be the same (For edge tracer, this will likely have the highest granularity. Is the line generated essentially (x,y) point pairs?).
