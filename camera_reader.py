# -*- coding:utf-8 -*-
import cv2

from boss_train import Model
from image_show import show_image

if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    cascade_path = "/home/dachuan/PycharmProjects/untitled1/haarcascade_frontalface_alt.xml"
    model = Model()
    model.load()
    while True:
        xiaonum=0
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
                cv2.imwrite('xiaochuan.jpg',image)
                result = model.predict(image)
                if result == 0:  # lishechuan
                    print('lishechuan in the home')
                    with open('warning.txt','w') as f:
                        a='0'
                        f.write(a)


                elif result== 1:
                    print('hongyi in the home')
                    with open('warning.txt','w+') as f:
                        a='1'
                        f.write(a)
                elif result== 2:
                    print('liuxiao in the home')
                    with open('warning.txt','w+') as f:
                        a='2'
                        f.write(a)

                # else:
                #     print('you wai ren jin ru')
                #     with open('warning.txt', 'w+') as f:
                #         a = '3'
                #         f.write(a)

        cv2.imshow("test", frame)  # 显示图像
        k = cv2.waitKey(100)

        if k == 27:
            break
    cap.release()
    cv2.destroyWindow("test")
