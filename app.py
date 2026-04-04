# attendance system - mini project
# K.Raghuveer
# started this around feb, kept breaking lol
# finally got deepface working after like 2 days of fighting with dlib

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import sqlite3
import base64
import os
import uuid
import cv2
from datetime import datetime, date

app = Flask(__name__, template_folder='templates')
CORS(app)

DB_PATH = 'attendance.db'
FACES_DIR = 'known_faces'
os.makedirs(FACES_DIR, exist_ok=True)

# deepface is optional - system still works without it (just no emotion/recognition)
# had a nightmare getting dlib to install on windows, switched to deepface instead
try:
    from deepface import DeepFace
    DEEPFACE_OK = True
except Exception as e:
    DEEPFACE_OK = False
    print("deepface not available:", e)
    print("install with: pip install deepface tf-keras")


# using haar cascade for detection - tried dnn model too but this was faster for realtime
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            roll_number TEXT,
            photo_path  TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # added emotion and attention_score for the behaviour analysis part
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id      INTEGER,
            date            DATE,
            time            TEXT,
            emotion         TEXT DEFAULT 'neutral',
            attention_score INTEGER DEFAULT 70,
            FOREIGN KEY (student_id) REFERENCES students(id),
            UNIQUE(student_id, date)
        )
    ''')

    conn.commit()
    conn.close()

init_db()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def decode_b64_image(b64_str):
    # webcam sends base64 with a prefix like "data:image/jpeg;base64,..."
    # need to strip that before decoding
    try:
        if ',' in b64_str:
            b64_str = b64_str.split(',')[1]
        raw = base64.b64decode(b64_str)
        arr = np.frombuffer(raw, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img  # may still be None if the bytes aren't a valid image
    except Exception:
        return None


# spent way too long debugging a json error - numpy int32 isnt serializable
# this just converts everything to plain python types before jsonify
def to_python_types(obj):
    if isinstance(obj, dict):
        return {k: to_python_types(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_python_types(i) for i in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    return obj


# emotion -> what to show on screen
# attention score is just a rough estimate based on emotion type
# not scientific, just for the project demo
EMOTION_TABLE = {
    'happy':    ('Engaged',    92, '#34c759'),
    'neutral':  ('Attentive', 75, '#3b82f6'),
    'surprise': ('Curious',   82, '#8b5cf6'),
    'sad':      ('Distracted',38, '#f59e0b'),
    'fear':     ('Anxious',   28, '#f97316'),
    'angry':    ('Frustrated',18, '#ef4444'),
    'disgust':  ('Disengaged',22, '#ec4899'),
}

def get_emotion_data(emo):
    key = (emo or 'neutral').lower()
    return EMOTION_TABLE.get(key, ('Attentive', 70, '#3b82f6'))


def detect_faces_in_frame(img):
    if img is None or img.size == 0:
        return []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # these scaleFactor and minNeighbors values worked best after some trial and error
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    boxes = []
    for (x, y, w, h) in faces:
        boxes.append((int(y), int(x + w), int(y + h), int(x)))
    return boxes


# -------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/status')
def status():
    return jsonify({
        'face_recognition': DEEPFACE_OK,
        'deepface': DEEPFACE_OK
    })


@app.route('/api/register', methods=['POST'])
def register_student():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request.'})
    name = data.get('name', '').strip()
    roll = data.get('roll_number', '').strip()
    img_b64 = data.get('image', '')

    if not name:
        return jsonify({'success': False, 'message': 'Please enter a name.'})
    if not img_b64:
        return jsonify({'success': False, 'message': 'No photo received.'})

    img = decode_b64_image(img_b64)
    if img is None:
        return jsonify({'success': False, 'message': 'Could not decode the image. Please try again.'})
    faces = detect_faces_in_frame(img)

    if not faces:
        return jsonify({'success': False, 'message': 'Couldnt detect a face. Try better lighting.'})

    conn = get_db()
    already_there = conn.execute(
        'SELECT id FROM students WHERE LOWER(name) = ?', (name.lower(),)
    ).fetchone()
    if already_there:
        conn.close()
        return jsonify({'success': False, 'message': f'{name} is already registered.'})

    # save the biggest face (closest to camera usually)
    top, right, bottom, left = max(faces, key=lambda f: (f[1] - f[3]) * (f[2] - f[0]))
    face_crop = img[max(0, top):bottom, max(0, left):right]

    safe_name = name.replace(' ', '_')
    ts = datetime.now().strftime('%d%m%Y_%H%M')
    photo_full = os.path.join(FACES_DIR, f'{safe_name}_{ts}.jpg')
    photo_face = os.path.join(FACES_DIR, f'{safe_name}_{ts}_crop.jpg')

    cv2.imwrite(photo_full, img)
    cv2.imwrite(photo_face, face_crop)

    conn.execute(
        'INSERT INTO students (name, roll_number, photo_path) VALUES (?, ?, ?)',
        (name, roll, photo_face)
    )
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': f'{name} enrolled!'})


@app.route('/api/detect', methods=['POST'])
def detect_and_mark():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'faces': []})
    img_b64 = data.get('image', '')
    if not img_b64:
        return jsonify({'success': False, 'faces': []})

    img = decode_b64_image(img_b64)
    if img is None:
        return jsonify({'success': False, 'faces': []})
    today = date.today().isoformat()
    now_time = datetime.now().strftime('%H:%M:%S')

    conn = get_db()
    all_students = conn.execute('SELECT id, name, photo_path FROM students').fetchall()
    conn.close()

    face_boxes = detect_faces_in_frame(img)
    output = []

    for (top, right, bottom, left) in face_boxes:
        face_crop = img[max(0, top):bottom, max(0, left):right]
        if face_crop.size == 0:
            continue

        matched_name = 'Unknown'
        matched_id = None
        emotion = 'neutral'

        # face matching using deepface verify
        # compares live face against each saved student photo
        # use a unique temp path per request to avoid race conditions
        if DEEPFACE_OK and len(all_students) > 0:
            tmp_path = f'_scan_tmp_{uuid.uuid4().hex}.jpg'
            cv2.imwrite(tmp_path, face_crop)
            best_dist = 999.0

            try:
                for s in all_students:
                    if not s['photo_path'] or not os.path.exists(s['photo_path']):
                        continue
                    try:
                        check = DeepFace.verify(
                            img1_path=tmp_path,
                            img2_path=s['photo_path'],
                            model_name='Facenet',
                            enforce_detection=False,
                            silent=True
                        )
                        dist = float(check.get('distance', 999))
                        if check.get('verified') and dist < best_dist:
                            best_dist = dist
                            matched_id = int(s['id'])
                            matched_name = str(s['name'])
                    except Exception:
                        # silently skip if deepface throws on a particular image
                        pass
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        # get emotion from face crop
        if DEEPFACE_OK:
            try:
                emo_data = DeepFace.analyze(
                    face_crop,
                    actions=['emotion'],
                    enforce_detection=False,
                    silent=True
                )
                if isinstance(emo_data, list):
                    emo_data = emo_data[0]
                emotion = str(emo_data.get('dominant_emotion', 'neutral'))
            except Exception:
                pass  # fallback to neutral

        label, score, color = get_emotion_data(emotion)

        # update attendance table - upsert so we dont get duplicates for same day
        if matched_id:
            conn = get_db()
            try:
                conn.execute('''
                    INSERT INTO attendance (student_id, date, time, emotion, attention_score)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(student_id, date) DO UPDATE SET
                        emotion = excluded.emotion,
                        attention_score = excluded.attention_score,
                        time = excluded.time
                ''', (matched_id, today, now_time, emotion, score))
                conn.commit()
            except Exception as err:
                print('attendance db write failed:', err)
            conn.close()

        output.append({
            'name': matched_name,
            'student_id': matched_id,
            'bbox': {
                'top': int(top),
                'right': int(right),
                'bottom': int(bottom),
                'left': int(left)
            },
            'emotion': emotion,
            'attention_label': label,
            'attention_score': int(score),
            'color': color,
        })

    return jsonify({'success': True, 'faces': to_python_types(output)})


@app.route('/api/attendance/today')
def get_todays_attendance():
    today = date.today().isoformat()
    conn = get_db()
    rows = conn.execute('''
        SELECT s.name, s.roll_number, a.time, a.emotion, a.attention_score
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE a.date = ?
        ORDER BY a.time ASC
    ''', (today,)).fetchall()
    conn.close()

    return jsonify({
        'success': True,
        'date': today,
        'count': len(rows),
        'students': [dict(r) for r in rows]
    })


@app.route('/api/students')
def get_all_students():
    conn = get_db()
    rows = conn.execute(
        'SELECT id, name, roll_number, created_at FROM students ORDER BY name ASC'
    ).fetchall()
    conn.close()
    return jsonify({'success': True, 'students': [dict(r) for r in rows]})


@app.route('/api/students/<int:sid>', methods=['DELETE'])
def remove_student(sid):
    conn = get_db()
    conn.execute('DELETE FROM attendance WHERE student_id = ?', (sid,))
    conn.execute('DELETE FROM students WHERE id = ?', (sid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


if __name__ == '__main__':
    print()
    print('EduScan - Classroom Attendance System')
    print('by K.Raghuveer | Mini Project')
    print('------------------------------------')
    print('deepface:', 'ready' if DEEPFACE_OK else 'NOT installed (pip install deepface tf-keras)')
    print('opencv:', 'ready')
    print('url: http://localhost:5000')
    print()
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode, port=5000)
