# -*- coding:utf-8 -*-
import cv2

#from boss_train import Model
from image_show import show_image

if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    cascade_path = "/home/dachuan/PycharmProjects/untitled1/haarcascade_frontalface_alt.xml"
    xiaonum = 0
    #model = Model()
    #model.load()
    while True:

        if xiaonum==301:
            print('over')
            break
        _, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(cascade_path)
        facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))
        #facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.01, minNeighbors=3, minSize=(3, 3))
        #cv2.imwrite('./data/dachuan/%s.jpg' % (str(num)), image)
        if len(facerect) > 0:
            print('face detected')
            color = (255, 255, 255)  # 白
            for rect in facerect:
                x, y = rect[0:2]
                width, height = rect[2:4]
                image = frame[y - 10: y + height, x: x + width]
                cv2.imwrite('./data/dachuan/%s.jpg' % (str(xiaonum)), image)

                xiaonum+=1
                print(xiaonum)
        cv2.imshow("test", frame)  # 显示图像
        k = cv2.waitKey(100)

        if k == 27:
            break
    cap.release()
    cv2.destroyWindow("test")
