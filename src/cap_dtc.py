from picamera2_t1 import CameraModule
from img_dtc_t1 import Detect

class Cap_Dtc:
    def __init__(self):
        self.camera=CameraModule()
        self.detector=Detect()

    def run(self):
        try:
            img=self.camera.cap()

            self.detector.dtc_img(img)

        except Exception as e:
            print("error:",e)

        # finally:
        #     self.camera.end()

    def end(self):
        self.camera.end()

def main():
    cap_dtc=Cap_Dtc()
    try:
        while True:
            cap_dtc.run()
            a=int(input("もう一度撮るなら1,終了はctrl+c:"))
            if a==1:
                continue
    except KeyboardInterrupt as e:
        print(e)
    finally:
        cap_dtc.end()

if __name__=='__main__':
    main()
