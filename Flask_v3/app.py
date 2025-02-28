from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/circle')
def circle():
    # Define the directory path where the image files are located
    image_dir = '/home/yash/PCB_FORGE/Flask_v3/inputs'
    # Get a list of image filenames in the specified directory
    image_files = [filename for filename in os.listdir(image_dir) if filename.endswith(('.jpg', '.png'))]
    return render_template('circle.html', image_filenames=image_files)

@app.route('/capture', methods=['POST'])
def capture():
    # Get the image name from the form submission
    image_name = request.form['imageName']
    # Run the capture_image.py script with the provided image name
    subprocess.run(['python3', 'capture_image.py', image_name])
    return 'Image captured and saved successfully!'

@app.route('/detect_circle', methods=['POST'])
def detect_circle():
    if request.method == 'POST':
        # Get the image name from the form submission
        image_name = request.form['imagePath']
        # Construct the full image path
        image_path = f'/home/yash/PCB_FORGE/Flask_v3/inputs/{image_name}'
        # Run detect_circle.py with the provided image path as an argument
        subprocess.run(['python3', 'detect_circle.py', image_path])
        return 'Circle detection completed!'
    #except Exception as e:
        #return f'An error occurred: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

