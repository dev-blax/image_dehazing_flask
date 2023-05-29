import sys
import cv2
import image_dehazer
import os
from datetime import datetime
# Check if the image path is provided as a command line argument
if len(sys.argv) < 2:
    print("Please provide the image path as a command line argument.")
    sys.exit(1)
image_path = sys.argv[1]
HazeImg = cv2.imread(image_path)
HazeCorrectedImg, HazeMap = image_dehazer.remove_haze(HazeImg)

folder_path = 'enhanced'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

imageName = f"dehazed_image_{timestamp}.jpg"

# Save the dehazed image in the "enhanced" folder
output_path = os.path.join(folder_path, imageName)
cv2.imwrite(output_path, HazeCorrectedImg)

print(output_path)
