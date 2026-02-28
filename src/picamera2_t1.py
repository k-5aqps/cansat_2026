from picamera2 import Picamera2
import time
import cv2
import numpy as np

class CameraModule:
    def __init__(self):
        self.picam2=Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration(main={"size": (1280, 720)}))
        self.cnt=0
        self.picam2.start()
    
    def cap(self):
        time.sleep(1)
        img=self.picam2.capture_array()
        img=cv2.flip(img,-1)
        self.cnt+=1
        #self.save(img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.save_bgr(img_bgr)
        return img_bgr
    
    #def save(self,img):
    #    cv2.imwrite(f"/home/pi/cansat_2026/img/test_cap/{self.cnt}.jpeg",img)

    def save_bgr(self,img_bgr):
        cv2.imwrite(f"/home/pi/cansat_2026/img/test_cap/{self.cnt}_BGR.jpeg",img_bgr) #保存した画像の確認。いらない画像は削除

    def end(self):
        self.picam2.stop()
        self.picam2.close()

def main():
    camera = CameraModule()
    camera.cap()

if __name__=="__main__":
    main()