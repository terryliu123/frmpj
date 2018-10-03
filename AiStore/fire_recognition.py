import cv2,numpy
def contrast_brightness_demo(image, c, b):  #其中c为对比度，b为每个像素加上的值（调节亮度）
    blank = numpy.zeros(image.shape, image.dtype)   #创建一张与原图像大小及通道数都相同的黑色图像
    dst = cv2.addWeighted(image, c, blank, 1-c, b) #c为加权值，b为每个像素所加的像素值
    ret, dst = cv2.threshold(dst, 25, 255, cv2.THRESH_BINARY)
    return dst


capture = cv2.VideoCapture("C:/pythondev/o.mp4")
redThre = 105
saturationTh = 42
while(True):
    ret, frame = capture.read()
    cv2.imshow("frame", frame)
    B = frame[:, :, 0]
    G = frame[:, :, 1]
    R = frame[:, :, 2]
    minValue = numpy.array(numpy.where(R <= G, numpy.where(G <= B, R, numpy.where(R <= B, R, B)), numpy.where(G <= B, G, B)))
    S = 1 - 3.0 * minValue / (R + G + B + 1)
    fireImg = numpy.array(numpy.where(R > redThre, numpy.where(R >= G, numpy.where(G >= B, numpy.where(S >= 0.2, numpy.where(S >= (255 - R)*saturationTh/redThre, 255, 0), 0), 0), 0), 0))
    gray_fireImg = numpy.zeros([fireImg.shape[0], fireImg.shape[1], 1], numpy.uint8)
    gray_fireImg[:, :, 0] = fireImg
    gray_fireImg = cv2.GaussianBlur(gray_fireImg, (7, 7), 0)
    gray_fireImg = contrast_brightness_demo(gray_fireImg, 5.0, 25)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    gray_fireImg = cv2.morphologyEx(gray_fireImg, cv2.MORPH_CLOSE, kernel)
    dst = cv2.bitwise_and(frame, frame, mask=gray_fireImg)
    cv2.imshow("fire", dst)
    cv2.imshow("gray_fireImg", gray_fireImg)
    c = cv2.waitKey(40)
    if c == 27:
        break