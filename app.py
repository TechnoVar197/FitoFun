from flask import Flask, request, jsonify
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import os

app = Flask(__name__)

# Define allowed file extensions
UPLOAD_FOLDER = 'uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the YOLO model
model_path = "ml/last.pt"  # Adjust path as necessary
model = YOLO(model_path)

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return jsonify(message="API is running")

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    image_file = request.files['image']

    # Check if the file has an allowed extension
    if not allowed_file(image_file.filename):
        return jsonify({'error': 'File type not allowed. Allowed extensions are: png, jpg, jpeg'}), 400

    # Securely save the uploaded file
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)

    # Read the saved image
    image = cv2.imread(image_path)

    if image is None:
        return jsonify({'error': 'The file is not a valid image'}), 400

    results = model.predict(source=image, show=False)
    detections = []

    try:
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_index = int(box.cls[0])  # Ensure this matches your model's output
                class_name = r.names[cls_index]
                detections.append(class_name)

        if detections:
            response = {'detected_objects': detections, 'count': len(detections)}
        else:
            response = {'message': 'No objects detected'}

        # Delete the file after processing
        os.remove(image_path)

        return jsonify(response), 200
    except Exception as e:
        # Delete the file in case of an error
        os.remove(image_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8000)
