import face_recognition

def detect_faces(img):
    face_locations = face_recognition.face_locations(img)
    return face_locations
