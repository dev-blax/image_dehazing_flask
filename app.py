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
        
        # Save the processed image to the static folder
        temp_filename = 'processed_image.png'
        static_folder = os.path.join(app.root_path, 'static')
        temp_filepath = os.path.join(static_folder, temp_filename)
        processed_image_pil.save(temp_filepath)
        
        # Pass the filename to the template for display
        return render_template('result.html', filename=temp_filename)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
