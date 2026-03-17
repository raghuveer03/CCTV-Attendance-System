# dev notes

personal notes while building this, keeping here for reference

---

### dlib nightmare (day 1-2)

originally tried to use face_recognition library which needs dlib.
dlib needs cmake + visual studio build tools on windows. spent literally 2 hours on this.
even after installing cmake it failed building the wheel.

tried:
- downloading pre-built .whl files → 404 links everywhere
- pipwin install dlib → some js2py error
- conda install -c conda-forge dlib → worked but messed up my other env

**fix: switched to deepface entirely. uses facenet model, no dlib needed.**

---

### int32 json error

was getting `TypeError: Object of type int32 is not JSON serializable`
when returning face detection results.

the issue was that opencv face detection returns numpy int32 for coordinates.
json.dumps cant handle that, needs plain python int.

added a `to_python_types()` function that recursively converts numpy types.
also cast coords to `int()` directly in `detect_faces_in_frame()`.

---

### camera mirroring issue

webcam video looks mirrored. when i capture a frame and send it to backend,
the face was still detected fine actually, but the bounding box drawn on canvas
was flipped.

fix: flip video with `transform: scaleX(-1)` in css.
when capturing frame for backend, mirror it back with ctx.scale(-1,1) first.

---

### deepface slow on first run

first scan takes 10-15 seconds because it downloads:
- facenet_weights.h5 (~92MB)  
- facial_expression_model_weights.h5 (~6MB)

after that cached in `C:\Users\<name>\.deepface\weights\`
subsequent scans are fast.

---

### todo (things i didnt finish)

- [ ] multiple photos per student for better accuracy
- [ ] export attendance to excel/csv
- [ ] weekly/monthly attendance reports
- [ ] notification if a student has low attention score consistently
- [ ] admin login so random people cant delete students

---

### things that actually work well

- the emotion → attention score mapping feels realistic in demos
- upsert query handles duplicate scans cleanly
- cascade detection is fast enough for 1.5s interval scanning

