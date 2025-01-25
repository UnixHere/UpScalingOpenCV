from flask import Flask, render_template, request, send_from_directory
import os
import io
from upscale import UpScale
import cv2
app = Flask(__name__,template_folder='template')

# Directory to store the uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to upscale the image
def upscale_image(image):
    return UpScale(image)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the file is part of the request
        if 'file' not in request.files:
            return render_template('index.html', error="No file selected.")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No file selected.")
        
        if file:
            # Save the file to the upload folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Upscale the image
            upscaled_image = upscale_image(filepath)
            # Save the upscaled image
            upscaled_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'upscaled_' + file.filename)
            cv2.imwrite(upscaled_filepath, upscaled_image)
            
            return render_template('index.html', image1=file.filename, image2='upscaled_' + file.filename)

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)