from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Define the directory path where the image files are located
    image_dir = '/home/yash/PCB_FORGE/Flask_v2'
    # Get a list of image filenames in the specified directory
    image_files = [filename for filename in os.listdir(image_dir) if filename.endswith(('.jpg', '.png'))]
    return render_template('index.html', image_filenames=image_files)

@app.route('/capture', methods=['POST'])
def capture():
    # Get the image name from the form submission
    image_name = request.form['imageName']
    # Run the capture_image.py script with the provided image name
    subprocess.run(['python3', 'capture_image.py', image_name])
    return 'Image captured and saved successfully!'

@app.route('/detect_circle', methods=['POST'])
def detect_circle():
    # Get the image path from the form submission
    image_path = request.form['imagePath']
    # Run the detect_circle.py script with the provided image path
    subprocess.run(['python3', 'detect_circle.py', image_path])
    return 'Circle detection completed!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

