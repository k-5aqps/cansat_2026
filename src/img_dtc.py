import cv2
import numpy as np
from logwrite import MyLogging   # 追加

low_color1=np.array([0,80,50])
hight_color1=np.array([5,255,255])
low_color2=np.array([170,80,50])
hight_color2=np.array([180,255,255])

class Detect():

    def __init__(self):
        self.cnt = 0
        self.log = MyLogging()   # ログ初期化

    def dtc_img(self, image):

        img = image

        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
        img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        bin_img1 = cv2.inRange(hsv, low_color1, hight_color1)
        bin_img2 = cv2.inRange(hsv, low_color2, hight_color2)
        mask = bin_img1 + bin_img2
        mask = cv2.medianBlur(mask, 5)
        masked_img = cv2.bitwise_and(img, img, mask=mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            self.log.write("検出不可（輪郭なし）", "WARNING")
            self.cnt += 1
            cv2.imwrite(f"/home/pi/cansat_2026/img_dtc/failed_none_{self.cnt}_result.jpg", masked_img)
            return "not find"

        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        x, y, w, h = cv2.boundingRect(largest_contour)
        vertex = ((x+w)+x)//2

        cv2.rectangle(masked_img, (x, y), (x+w, y+h), (255,20,147), 1)

        if area < 300:
            self.log.write(f"検出不可 面積不足 area={area}", "WARNING")
            self.cnt += 1
            cv2.imwrite(f"/home/pi/cansat_2026/img_dtc/failed_area_{self.cnt}_result.jpg", masked_img)
            return "not find"

        self.cnt += 1
        cv2.imwrite(f"/home/pi/cansat_2026/img_dtc/{self.cnt}_result.jpg", masked_img)

        area_ratio = area/(1280*720)

        if area_ratio > 0.7:
            self.log.write("dir: goal", "INFO")
            return "goal"

        if 0 < vertex < 426:
            self.log.write(f"dir: left, vertex:{vertex}", "INFO")
            return "left"

        elif 426 <= vertex < 853:
            self.log.write(f"dir: forward, vertex:{vertex}", "INFO")
            return "forward"

        elif 853 <= vertex < 1280:
            self.log.write(f"dir: right, vertex:{vertex}", "INFO")
            return "right"