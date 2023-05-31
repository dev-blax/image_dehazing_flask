from flask import Flask, render_template, request
from PIL import Image
import cv2
import image_dehazer
import numpy as np
import os

app = Flask(__name__)

def dehaze_image(image):
    image, HazeMap = image_dehazer.remove_haze(image)
    
    return image

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded image from the form
        uploaded_file = request.files['image']
        
        # Open and process the image
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        processed_image = dehaze_image(image)

        # Convert the processed image back to PIL format
        processed_image_pil = Image.fromarray(processed_image)
        
        # Save the images to the static folder
        static_folder = os.path.join(app.root_path, 'static')
        original_image_filepath = os.path.join(static_folder, 'original_image.png')
        processed_image_filepath = os.path.join(static_folder, 'processed_image.png')
        original_image_pil.save(original_image_filepath)
        processed_image_pil.save(processed_image_filepath)
        
        # Pass the filenames to the template for display
        return render_template('index.html', original_image=original_image_filepath, processed_image=processed_image_filepath)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
