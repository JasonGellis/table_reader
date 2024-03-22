from flask import Flask, request, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from web.read_and_process import read_images, process_image  # Assuming process_image is another function you want to use

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handle file uploads and processing."""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            return render_template('index.html', message='No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Process the image
            processed_image_path = read_images(filepath)  # Modify this according to how you want to use the function
            # Assuming read_images or another function returns the path of the processed image
            return send_from_directory(directory=os.path.dirname(processed_image_path), filename=os.path.basename(processed_image_path), as_attachment=True)
    # If not a POST request, show the upload form.
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)