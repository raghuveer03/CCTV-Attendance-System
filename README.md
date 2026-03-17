# Classroom Attendance & Behaviour Analysis

Mini project for my 3rd year — automatic attendance using face recognition + real-time student behaviour analysis from webcam.

**By K.Raghuveer
k.dheekshith
 m. sreevalli
 **


---

## Background

Was tired of manual attendance being a waste of 5-10 minutes every class. This marks it automatically when students sit in front of the webcam. Also tracks if students look distracted, frustrated, happy etc. as a bonus feature for behaviour analysis.

No CCTV required — just runs on a laptop/PC with a webcam.

---

## Features

- Enroll students with their photo (once)
- Live webcam scanning marks attendance automatically
- Emotion detection (happy, sad, angry, neutral, etc.)
- Attention score calculated per student based on their emotion
- Today's attendance list with behaviour summary

---

## Tech Used

| Component | Library |
|-----------|---------|
| Backend | Flask (Python) |
| Face Detection | OpenCV Haar Cascade |
| Face Recognition | DeepFace + Facenet model |
| Emotion Detection | DeepFace |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript (no framework) |

---

## How to Run

**Requirements: Python 3.10 or 3.12**

```bash
git clone https://github.com/kraghuveer/classroom-attendance-system.git
cd classroom-attendance-system

pip install flask flask-cors opencv-python numpy deepface tf-keras

python app.py
```

Open browser → `http://localhost:5000`

> On first scan, DeepFace downloads model weights (around 90MB). This only happens once.

---

## How It Works

**Enrolling:**
1. Start webcam in "Enroll Student" tab
2. Capture photo
3. Enter name + roll number
4. System saves cropped face photo to `known_faces/`

**Attendance:**
1. Go to "Mark Attendance" tab
2. Click Start Scanning
3. Every 1.5 seconds, it sends the webcam frame to backend
4. Backend detects faces → compares each face to saved student photos using Facenet
5. Match found → marks present in SQLite with timestamp + emotion

**Behaviour Analysis:**
- DeepFace detects dominant emotion from each face crop
- Emotion is mapped to an attention score (happy = 92%, angry = 18% etc.)
- Shown in the "Present Students" tab

---

## Project Structure

```
├── app.py                  # flask backend + all api routes
├── templates/
│   └── index.html          # entire frontend
├── known_faces/            # student face photos (auto-created, gitignored)
├── attendance.db           # sqlite db (auto-created, gitignored)
├── requirements.txt
└── setup.md                # detailed setup steps for windows
```

---

## Limitations

- Works best with good lighting, direct face angle
- One photo per student — accuracy improves with more photos but didn't implement that yet
- Emotion detection can be inaccurate sometimes, it's not perfect
- Doesn't work through glasses very well
- First scan is slow because models load on demand

---

## Screenshots

*(to be added)*

---

## References

- DeepFace library: https://github.com/serengil/deepface
- OpenCV Haar Cascades: https://docs.opencv.org
- Facenet paper (face recognition model used)

