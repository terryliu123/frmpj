import  cv2

video_capture = cv2.VideoCapture(0)
video_capture1 = cv2.VideoCapture(1)
video_capture2 = cv2.VideoCapture(2)
videodict=[video_capture,video_capture1,video_capture2]
while True:

    ret, frame = videodict[0].read()
    ret1, frame1 = videodict[1].read()
    ret2, frame2 = videodict[2].read()
    cv2.imshow("aaa",frame)
    cv2.imshow("aaa1", frame1)
    cv2.imshow("aaa2", frame2)
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()