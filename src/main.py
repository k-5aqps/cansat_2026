import pyserial_t1
import picamera2_t1
import img_dtc_t1
import logwrite
import motor

gps=pyserial_t1.GPSModule()
cm=picamera2_t1.CameraModule()
img=img_dtc_t1.Detect()
log=logwrite.MyLogging()
mv=motor.MotorController()

def main():
    mv.move("forward",4,80)