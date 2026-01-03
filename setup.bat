@echo off
mkdir haarcascades
curl -o haarcascades\haarcascade_frontalface_default.xml https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
curl -o haarcascades\haarcascade_mouth.xml https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_mouth.xml
pip install -r requirements.txt
echo Setup complete! Run data_collection.py first, then train_model.py, then main_attendance_cctv.py
pause

