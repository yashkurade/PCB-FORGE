from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = '/home/yash/PCB_FORGE/Flask_v7/uploads'
COORDINATES_FOLDER = '/home/yash/PCB_FORGE/Flask_v7/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COORDINATES_FOLDER'] = COORDINATES_FOLDER

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/circle')
def circle():
    # Define the directory path where the image files are located
    image_dir = '/home/yash/PCB_FORGE/Flask_v7/inputs'
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
        image_path = f'/home/yash/PCB_FORGE/Flask_v7/inputs/{image_name}'
        # Run detect_circle.py with the provided image path as an argument
        subprocess.run(['python3', 'detect_circle.py', image_path])
        return 'Circle detection completed!'
    #except Exception as e:
        #return f'An error occurred: {str(e)}'
        
@app.route('/detect_rectangle', methods=['POST'])
def detect_rectangle():
    image_name = request.form['imagePath']
    image_path = os.path.join('/home/yash/PCB_FORGE/Flask_v7/inputs', image_name)
    subprocess.run(['python3', 'pad_detector.py', image_path])
    return 'Rectangle detection completed!'

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            return 'No file part'

        file = request.files['image']
        new_filename = request.form['filename']

        # Check if the user submitted a file
        if file.filename == '':
            return 'No selected file'

        # Check if the file is allowed
        if file and allowed_file(file.filename):
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            new_filename = secure_filename(new_filename) + '.' + file_ext
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            # Redirect to process_negative.html after successful upload
            return redirect(url_for('process_negative'))

        return 'Invalid file type'

    return render_template('upload.html')

@app.route('/process_negative', methods=['GET', 'POST'])
def process_negative():
    if request.method == 'POST':
        image_filename = request.form['imageFile']  # Get the selected image filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)

        # Here you can implement your logic to process the selected image
        subprocess.run(['python3', 'uploaded_pad_detect.py', image_path])

        return f'Image processing completed for {image_filename}'

    # Get a list of image filenames in the upload folder
    image_files = [filename for filename in os.listdir(UPLOAD_FOLDER) if filename.endswith(('.jpg', '.png', '.jpeg'))]

    return render_template('process_negative.html', image_filenames=image_files)

@app.route('/solder', methods=['GET', 'POST'])
def solder():
    if request.method == 'POST':
        # Get the coordinates from the form submission
        coordinates_filename = request.form['coordinatesFile']
        # Construct the full coordinates path
        coordinates_path = os.path.join(app.config['COORDINATES_FOLDER'], coordinates_filename)
        # Run solder.py with the provided coordinates path as an argument
        subprocess.run(['python3', 'solder.py', coordinates_path])
        return 'Soldering completed!'

    # Get a list of coordinates filenames in the coordinates folder
    coordinates_files = [filename for filename in os.listdir(COORDINATES_FOLDER) if filename.endswith('.txt')]

    return render_template('solder_page.html', coordinates_filenames=coordinates_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
