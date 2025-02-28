from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    # Get the image name from the form submission
    image_name = request.form['imageName']
    # Run the capture_image.py script with the provided image name
    subprocess.run(['python3', 'capture_image.py', image_name])
    return 'Image captured and saved successfully!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
