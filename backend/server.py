from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load reference image of authorized person
ref_img = cv2.imread("authorized.jpg", cv2.IMREAD_GRAYSCALE)
ref_img = cv2.resize(ref_img, (100, 100))  # Normalize size

def is_authorized_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100))

        # Compare with reference image using Mean Squared Error
        diff = np.sum((face.astype("float") - ref_img.astype("float")) ** 2)
        diff /= float(face.shape[0] * face.shape[1])

        if diff < 2000:  # Threshold (tweak as needed)
            return True

    return False


@app.route('/verify', methods=['POST'])
def verify():
    file = request.files['image'].read()
    npimg = np.frombuffer(file, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if is_authorized_face(frame):
        return jsonify({"status": "OPEN"})
    else:
        return jsonify({"status": "DENIED"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
