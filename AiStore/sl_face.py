# read the images and it's image name then pre-encoding 2018.6.23
print("Initialing...")
import os,cv2
import time
import pickle
import face_recognition

def saveface():
    time_start = time.time()
    img_path = os.path.join('static/images')  # 存储的路径
    img_path ='C:/pythondev/FrmPJ/static/images'
    os.chdir(img_path+"/face")
    images_file = os.listdir('.')
    know_names = []
    know_paths = []
    know_encodings = []
    print("Reading files from directory...")
    for each in images_file:
        name = os.path.splitext(each)[0]
        know_names.append(name)
        image_path = img_path + '/face/' + each
        print(image_path)
        know_paths.append(image_path)
    print("Starting encoding!")
    # print(know_names)
    # print(know_paths)
    count = 1
    for each_path in know_paths:
        img = face_recognition.load_image_file(each_path)
        # locate face and detection_method
        print("Encoding the %d picture..." % count)
        # boxes = face_recognition.face_locations(img,model = 'cnn')#hog faster,and cnn more accurate
        encoding = face_recognition.face_encodings(img)[0]
        # encoding = face_recognition.face_encodings(img,boxes)
        know_encodings.append(encoding)
        count = count + 1
    # 原文中采用字典存储，写入了一个文件，我把它俩分开了
    print("Finished encodings,Writing pickle file...")
    # dump images encodings in to face_encodings.pkl file

    pickle_encoding_file = open(img_path+'/facepkl/face_encodings.pkl', 'wb')
    pickle.dump(know_encodings, pickle_encoding_file)
    pickle_encoding_file.close()

    # dump images names in to face_names.pkl file
    pickle_name_file = open(img_path+'/facepkl/face_names.pkl', 'wb')
    pickle.dump(know_names, pickle_name_file)
    pickle_name_file.close()
    time_end = time.time()
    time_take = time_end - time_start
    print("It takes %s seconds!" % time_take)
    print("All images pretreatment finished!")

def loadface(imgpath):
    know_names = []
    know_encodings = []
    # ---------------------------------------------------------------
    img_path = os.path.join('static/images/facepkl')  # 存储的路径
    f = open(img_path+'/face_names.pkl', 'rb')
    know_names = pickle.load(f)  # 读出文件的数据个数
    f.close()
    f1 = open(img_path+'/face_encodings.pkl', 'rb')
    know_encodings = pickle.load(f1)  # 读出文件的数据个数
    f1.close()
    # --------------------------------------------------------------
    face_locations = face_recognition.load_image_file(imgpath)
    face_encodings = face_recognition.face_encodings(face_locations)
    face_names = []
    print(know_names)
    # -------------------------------------------------------------------
    for face_encoding in face_encodings:
        # 默认为unknown
        matches = face_recognition.compare_faces(know_encodings, face_encoding)
        name = "Unknown"
        print(matches)
        if True in matches:
            first_match_index = matches.index(True)
            name = know_names[first_match_index]
        face_names.append(name)
    print(face_names)
    return face_names

# saveface()