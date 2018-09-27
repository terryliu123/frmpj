import face_recognition

def checkface(imgpath):
    # Load the jpg files into numpy arrays
    biden_image = face_recognition.load_image_file("C:/pythondev/my.jpg")
    obama_image = face_recognition.load_image_file("C:/pythondev/obama.jpg")
    # unknown_image = face_recognition.load_image_file(imgpath)
    unknown_image =face_recognition.load_image_file(imgpath)
    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
    try:
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)
    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        quit()

    known_faces = [
        biden_face_encoding,
        obama_face_encoding
    ]
    name=""
    for face_location in unknown_face_encoding:
        results = face_recognition.compare_faces(known_faces, face_location)
        if results[0]==True :
            name="terry"
            print("terry")
        elif results[1]==True:
            name="Obama"
            print("Obama")
        else:
            print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
    return name
