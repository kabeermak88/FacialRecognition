from flask import Flask, render_template, request, jsonify
import face_recognition
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare_faces():
    if "image1" not in request.files or "image2" not in request.files:
        return jsonify({"error": "Both image files are required"}), 400

    file1 = request.files["image1"]
    file2 = request.files["image2"]

    if file1.filename == "" or file2.filename == "":
        return jsonify({"error": "Files must have valid names"}), 400

    path1 = os.path.join(app.config["UPLOAD_FOLDER"], file1.filename)
    path2 = os.path.join(app.config["UPLOAD_FOLDER"], file2.filename)

    file1.save(path1)
    file2.save(path2)

    try:
        image1 = face_recognition.load_image_file(path1)
        image2 = face_recognition.load_image_file(path2)

        encodings1 = face_recognition.face_encodings(image1)
        encodings2 = face_recognition.face_encodings(image2)

        # Check if faces are found
        if len(encodings1) == 0 or len(encodings2) == 0:
            return jsonify({"error": "No face detected in one or both images"}), 400

        match = face_recognition.compare_faces([encodings1[0]], encodings2[0])[0]

        return jsonify({"result": "✅ Match!" if match else "❌ No Match!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
