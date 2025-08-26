# Smart Door Lock using ESP32 and Flask (OpenCV-based)

This project implements a **smart door lock system** using an **ESP32-CAM module** and a **Flask server with OpenCV**.
The ESP32 captures an image and sends it to the Flask server. The Flask server processes the image, performs simple face detection/verification using OpenCV, and returns a response. Based on this response, the ESP32 decides whether to **unlock or keep the door locked**.

---

## 🚀 Features

* ESP32-CAM captures real-time images.
* Flask server processes images using **OpenCV** (no `cmake` or heavy dependencies required).
* Face verification against a **reference image**.
* ESP32 unlocks the door if a match is detected.
* Lightweight and works on LAN (local network).

---

## 📂 Project Structure

```
Smart-Door-Lock-Using-ESP32-and-Flask/
│── backend/
│   ├── server.py         # Flask server with OpenCV face detect
│── known_faces/
│   ├── reference.jpg     # Reference image of authorized person
│── sketch_aug22a/
│   ├── sketch_aug22a.ino # ESP32-CAM Arduino sketch
|   ├── camera_pins.h     # camera pins
|   ├── secrets.h         # Wifi cerrenditials (You should create your own to protect your env variables)
│── venv/                 # Python virtual environment
│── README.md             # Documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ ESP32-CAM Setup

1. Install **Arduino IDE**.
2. Add the ESP32 board manager in Arduino IDE:
   `File > Preferences > Additional Board Manager URLs:`

   ```
   https://dl.espressif.com/dl/package_esp32_index.json
   ```
3. Select board: `AI Thinker ESP32-CAM`.
4. Upload the provided `esp32_doorlock.ino` code.
5. Update the server **IP address** in the ESP32 code with your Flask server’s local IP.

---

### 2️⃣ Flask Server Setup

#### Step 1: Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On Linux/Mac
```

#### Step 2: Install Dependencies

```bash
pip install flask opencv-python
```

#### Step 3: Place a Reference Image

Save an image of the authorized person as `reference.jpg` inside `backend/`.

#### Step 4: Run the Server

```bash
cd backend
python server.py
```

You should see:

```
* Running on http://192.168.x.x:5000
```

---

### 3️⃣ ESP32 & Flask Communication

* ESP32 sends captured image → Flask server (`/verify` endpoint).
* Flask compares image with `reference.jpg`.
* Server responds:

  * `200 OK + "Authorized"` → ESP32 unlocks.
  * `401 Unauthorized` → ESP32 keeps locked.
* If Flask server is not running, ESP32 will return:

  ```
  HTTP Response code: -1
  ```

---

## 🛠️ Troubleshooting

* **OpenCV Resize Error (`!ssize.empty()`)**
  → Check that `reference.jpg` exists in `backend/`.
  → Ensure the path is correct.
* **ESP32 Error: `HTTP Response code: -1`**
  → Flask server is not running or wrong IP address.
  → Run `ipconfig` (Windows) or `ifconfig` (Linux/Mac) to find your local IP.
  → Replace it in ESP32 code.
* **Port Issues**
  → Default Flask runs on `5000`. Make sure your ESP32 requests `http://<PC-IP>:5000/verify`.

---

## 📌 Future Improvements

* Use ML-based face recognition (TensorFlow Lite, Mediapipe).
* Add multiple authorized users.
* Secure with HTTPS & authentication tokens.
* Integrate with mobile app for remote access.

---

## 🤝 Contribution

Pull requests are welcome! If you find bugs, feel free to open an issue.

