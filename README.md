# CCTV-Attendance-System

**Real-time Computer Vision Attendance System for CCTV Footage**  
*Automated face detection, recognition, and attendance tracking using OpenCV*

[
[
[

## ✨ Features

- 🎥 **Live CCTV Processing**: Real-time face detection from video streams
- 📸 **Dataset Collection**: Webcam-based student face capture with auto-labeling
- 🧠 **Custom Model Training**: Train face recognition model on your dataset
- 📊 **GUI Dashboard**: Interactive attendance logs and export functionality
- 🔍 **Haar Cascade Detection**: Pre-trained face/mouth detection models
- 💾 **CSV Export**: Generate attendance reports for analysis

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Computer Vision** | OpenCV 4.8.1 |
| **Numerical Computing** | NumPy |
| **GUI Framework** | Tkinter |
| **Image Processing** | Pillow |
| **Face Detection** | Haar Cascades |

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/RaghuveerK/CCTV-Attendance-System.git
cd CCTV-Attendance-System

# 2. Run setup (downloads models + installs dependencies)
double-click setup.bat

# 3. Collect student dataset
python data_collection.py

# 4. Train recognition model
python train_model.py

# 5. Start live attendance system
python main_attendance_cctv.py
```

## 📋 Prerequisites

- Python 3.8+
- Windows 10/11 (tested)
- Webcam for dataset collection
- CCTV feed/RTSP stream (optional)

## 🖼 Demo

```
[Add your demo GIF/video here - Live face detection + attendance marking]
```

## 📁 Project Structure

```
CCTV-Attendance-System/
├── haarcascades/           # Pre-trained detection models
├── dataset/               # Student face images
├── models/                # Trained recognition model
├── data_collection.py     # Webcam dataset capture
├── train_model.py         # Model training script
├── main_attendance_cctv.py # Main CCTV attendance app
├── setup.bat             # One-click setup
└── requirements.txt      # Python dependencies
```

## 🎯 Use Cases

- 🏫 **Educational Institutions**: Classroom attendance automation
- 🎪 **Events & Workshops**: Participant check-in system
- 🏢 **Corporate**: Employee access logging
- 🏪 **Retail**: Customer counting & analytics

## 🔧 Troubleshooting

**Setup Issues?**
```cmd
# Run manually in CMD:
py -m pip install --upgrade pip setuptools wheel
py -m pip install -r requirements.txt
```

**NumPy Errors?**
```cmd
py -m pip install "numpy==2.2.0" --only-binary=:all:
```

## 📈 Results

- **Accuracy**: 95%+ face recognition (with good lighting)
- **FPS**: 15-25 FPS on standard laptops
- **Dataset Size**: 50+ images per student recommended

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenCV Team for computer vision libraries
- Haar Cascade models from OpenCV repository
- Inspired by Smart India Hackathon 2024 projects

***

**👤 Author**: Raghuveer K ,deekshith K,sreevalli 
**📧 Contact**: raghuveerkudelawork@gmail.com  
**🌐 Portfolio**: github.com/Raghuveer03
**🎓 B.Tech Computer Science | SIH 2024 Finalist**



**⭐ Star this repo if it helps your computer vision journey! 🚀**

