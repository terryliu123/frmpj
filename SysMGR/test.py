import face_recognition
import pickle
imgpath="C:/pythondev/images/biden.jpg"
know_names = []
know_encodings = []
f = open('C:/pythondev/images/face_names.pkl', 'rb')
know_names = pickle.load(f)  # 读出文件的数据个数
f.close()
f1 = open('C:/pythondev/images/face_encodings.pkl', 'rb')
know_encodings = pickle.load(f1)  # 读出文件的数据个数
f.close()
face_locations = face_recognition.load_image_file(imgpath)
face_encodings = face_recognition.face_encodings(face_locations)
face_names = []
print(know_encodings)
for face_encoding in face_encodings:
    # 默认为unknown
    matches = face_recognition.compare_faces(know_encodings, face_encoding)
    name = "Unknown"
    if True in matches:
        first_match_index = matches.index(True)
        name = know_names[first_match_index]
    face_names.append(name)
print(face_names)