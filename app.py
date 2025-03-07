import os
import json
import dlib
import cv2
import numpy as np
from flask import Flask, request, render_template, jsonify

# Initialize Flask app
app = Flask(__name__)

# Paths to DLib models
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
FACE_RECOGNITION_MODEL_PATH = "dlib_face_recognition_resnet_model_v1.dat"

# Check if models exist
for model in [PREDICTOR_PATH, FACE_RECOGNITION_MODEL_PATH]:
    if not os.path.exists(model):
        raise FileNotFoundError(f"Error: {model} not found! Place it in the project folder.")

# Load models
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(PREDICTOR_PATH)
facerec = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL_PATH)

# Function to process images
def get_face_encoding(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detections = detector(img)

    if len(detections) == 0:
        return None

    shape = sp(img, detections[0])
    return np.array(facerec.compute_face_descriptor(img, shape))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    file1 = request.files['image1']
    file2 = request.files['image2']

    file1_path = os.path.join("uploads", file1.filename)
    file2_path = os.path.join("uploads", file2.filename)
    
    file1.save(file1_path)
    file2.save(file2_path)

    enc1 = get_face_encoding(file1_path)
    enc2 = get_face_encoding(file2_path)

    if enc1 is None or enc2 is None:
        return jsonify({"status": "error", "message": "No face detected in one or both images."})

    similarity = np.linalg.norm(enc1 - enc2)
    confidence = max(100 - (similarity * 100), 0)  # Convert distance to confidence %

    result = "The two faces belong to the same person." if confidence > 50 else "Faces do not match."
    
    return jsonify({
        "status": "success",
        "message": result,
        "confidence": round(confidence, 3)
    })

if __name__ == '__main__':
    app.run(debug=True)
