## Windows Setup

step by step if you're on windows and getting errors

### 1. check python version
```
python --version
```
need 3.10 or 3.12. 3.11 might have issues with tf-keras.

### 2. go into the project folder
```
cd path\to\classroom-attendance-system
```

### 3. install packages
```
pip install flask flask-cors opencv-python numpy deepface tf-keras
```

this takes a while. deepface pulls in tensorflow + keras.

### 4. test your camera first (optional but helpful)
```
python test_camera.py
```
green boxes should appear around your face. q to quit.

### 5. run the app
```
python app.py
```

open chrome → `http://localhost:5000`

---

### common errors i hit

**`No module named flask_cors`**
```
pip install flask-cors
```

**`Object of type int32 is not JSON serializable`**  
make sure you have the latest app.py

**first scan is super slow / hangs**  
normal. deepface is downloading model files (~100MB total). wait for it.
check terminal, it shows download progress.

**face not detected / wrong person matched**  
- lighting matters a lot. face the light, dont have it behind you
- look straight at camera when enrolling
- re-enroll if recognition is bad

**`can't open file app.py`**  
you're in the wrong folder. the file is one level deeper:
```
cd classroom_attendance   ← do this extra cd
python app.py
```

