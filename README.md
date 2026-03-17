<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&lines=Classroom+Attendance+System;Face+Recognition+%2B+AI+Behaviour;No+CCTV+Required+%F0%9F%8E%93" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv&logoColor=white)
![DeepFace](https://img.shields.io/badge/DeepFace-AI-orange?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite&logoColor=white)

<br/>

> **Automatic attendance marking using face recognition + real-time student behaviour analysis from webcam.**
> No CCTV. No hardware. Just a laptop.

<br/>

**By K.Raghuveer &nbsp;·&nbsp; K.Dheekshith &nbsp;·&nbsp; M.Sreevalli**

*3rd Year Mini Project*

<br/>

</div>

---

## 🧠 Why we built this

Manual attendance takes 5–10 minutes every class. For a college with 6+ periods a day, that's a lot of wasted time. We wanted something that just works automatically — student sits down, camera sees them, marked present.

The behaviour analysis part (emotion + attention score) was added as an extra feature to make it more useful for faculty — they can see if students are engaged, distracted, or frustrated during a lecture.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 👤 **Enroll Students** | Capture face photo once via webcam |
| 📡 **Auto Attendance** | Live scan every 1.5s, marks present automatically |
| 😊 **Emotion Detection** | Detects happy, sad, angry, neutral, fear, disgust |
| 🧠 **Attention Score** | Calculates engagement % based on emotion |
| 📊 **Live Dashboard** | See who's present today with behaviour summary |
| 🔍 **Search & Filter** | Search students in today's attendance list |

---

## 🛠️ Tech Stack

```
Backend      →  Flask (Python)
Detection    →  OpenCV Haar Cascade
Recognition  →  DeepFace + Facenet model
Emotions     →  DeepFace
Database     →  SQLite
Frontend     →  HTML + CSS + Vanilla JS (no framework)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or 3.12
- Webcam

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/raghuveer03/CCTV-Attendance-System.git
cd CCTV-Attendance-System

# 2. Install dependencies
pip install flask flask-cors opencv-python numpy deepface tf-keras

# 3. Run
python app.py
```

Then open your browser → **http://localhost:5000**

> 💡 First scan downloads DeepFace model weights (~90MB). Only happens once, cached after that.

---

## 🗂️ Project Structure

```
📦 classroom-attendance-system
 ├── 📄 app.py                 ← Flask backend + all API routes
 ├── 📁 templates/
 │   └── 📄 index.html         ← Complete frontend (single file)
 ├── 📁 known_faces/           ← Student photos saved here (gitignored)
 ├── 🗃️  attendance.db         ← SQLite database (auto-created)
 ├── 📄 requirements.txt
 ├── 📄 setup.md               ← Windows setup guide
 └── 📄 dev_notes.md           ← Notes from development
```

---

## 📖 How It Works

### Step 1 — Enroll a Student
```
Open webcam → Capture photo → Enter name & roll number → Save
```
System saves a cropped face photo to `known_faces/` folder.

### Step 2 — Mark Attendance
```
Start scanning → Every 1.5s, frame sent to backend
→ Faces detected → Compared against saved photos (Facenet)
→ Match found → Marked present with timestamp
```

### Step 3 — Behaviour Analysis
```
DeepFace analyzes each face crop → Dominant emotion detected
→ Mapped to attention score → Shown in dashboard
```

**Emotion → Attention Score mapping:**

| Emotion | Label | Score |
|---------|-------|-------|
| 😊 Happy | Engaged | 92% |
| 😐 Neutral | Attentive | 75% |
| 😲 Surprise | Curious | 82% |
| 😢 Sad | Distracted | 38% |
| 😨 Fear | Anxious | 28% |
| 😠 Angry | Frustrated | 18% |
| 🤢 Disgust | Disengaged | 22% |

---

## ⚠️ Known Limitations

- Works best with **good lighting** and direct face angle
- Currently stores **one photo per student** (more photos = better accuracy)
- Emotion detection isn't 100% accurate — used for demo/analysis only
- Doesn't work great through glasses
- First scan is slow (model loading)

---

## 🔮 Future Improvements

- [ ] Multiple photos per student for better accuracy
- [ ] Export attendance to Excel/CSV
- [ ] Weekly and monthly attendance reports
- [ ] Admin login / authentication
- [ ] Email alerts for low attendance

---

## 📚 References

- [DeepFace](https://github.com/serengil/deepface) — face recognition & emotion detection
- [OpenCV Haar Cascades](https://docs.opencv.org) — face detection
- [Facenet Paper](https://arxiv.org/abs/1503.03832) — recognition model used

---

<div align="center">

Made with ☕ and a lot of debugging &nbsp;·&nbsp; K.Raghuveer, K.Dheekshith, M.Sreevalli

*3rd Year Mini Project · 2024*

</div>
