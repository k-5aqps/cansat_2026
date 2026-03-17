import time
import cv2
import numpy as np
import config
from buzzer import BUZZER
from buzzer_pigpio import init,read_music
from logwrite import MyLogging
from start import awaiting
from motor_t1 import MotorController
from dtc_motor import Dtc_MotorController
from pyserial_t1 import GPSModule, calculate_target_distance_angle
from picamera2_camera import CameraModule
from img_dtc import Detect
import threading

class CanSatController:
    def __init__(self):
        self.log = MyLogging()
        self.motor = MotorController()
        self.dtc_motor = Dtc_MotorController()
        self.gps = GPSModule()
        self.camera = CameraModule()
        self.detector = Detect()
        self.stop_event = threading.Event()
        self.buzzer = BUZZER()

        # configからの設定値
        self.goal_coordinate = {"lat": config.GOAL_LAT, "lon": config.GOAL_LON}
        self.transition_dist = 18.0  # 18m以下でカメラフェーズへ
        self.target_dist = config.TARGET_DISTANCE
    
    def start_timer(self, limit_sec):
        def timer_thread():
            time.sleep(limit_sec)
            self.log.write("Mission Time Out (18min)", "WARNING")
            self.log.write("=== CanSat Finish ===","INFO")
            hz=[1048,987,880,783,698,659,587,523]
            for num in hz:
                self.buzzer.beep(0.5,num)
                time.sleep(0.01)
            self.stop_event.set()

        threading.Thread(
            target=timer_thread,
            daemon=True
        ).start()

    def run_mission(self):
        self.log.write("CanSat Start", "INFO")
        
        try:
            # 1. 待機フェーズ (start.py)
            self.log.write("Awaiting Start", "INFO")
            awaiting()
            self.start_timer(18 * 60)#18 * 60

            self.motor.move("forward",8,70)

            # 2. GPS誘導フェーズ
            self.run_gps_phase()
            cnt=0
            while cnt<5:
                self.buzzer.beep(0.5,1048)
                time.sleep(0.05)
                cnt+=1

            # 3. カメラ誘導フェーズ
            self.run_camera_phase()

            self.log.write("All Phase Complete","INFO")
            read_music("dango.csv")

        except KeyboardInterrupt:
            self.log.write("ユーザー操作により中断されました", "WARNING")
        except Exception as e:
            self.log.write(f"致命的なエラー: {e}", "CRITICAL")
            self.buzzer.beep(5,1048)
            self.log.write("CanSat Error Finish","INFO")
            self.log.write("Finish")
            read_music("dango.csv")
        finally:

            self.cleanup()

    def run_gps_phase(self):
        self.log.write(f"Start GPS Phase", "INFO")
        self.gps.connect()
        previous_coordinate = None

        while not self.stop_event.is_set():
            lat, lon, satellites, utc_time, dop = self.gps.get_gps_data()

            if lat is None or lon is None:
                continue

            # 衛星数チェック
            if satellites is not None and satellites < config.MIN_SATELLITES:
                self.log.write("Satellite不足", "WARNING")
                continue

            current_coordinate = {"lat": lat, "lon": lon}

            self.log.write(f"Current: lat={lat:.6f}, lon={lon:.6f}, sat={satellites}, dop={dop}","INFO")
            self.log.forCSV(lat, lon)

            # 初回移動（方位確定用）
            if previous_coordinate is None:
                self.motor.move("forward", 5, 60)
                previous_coordinate = current_coordinate
                continue

            # 距離と方向の計算
            nav = calculate_target_distance_angle(
                current_coordinate, previous_coordinate, 
                self.goal_coordinate, self.target_dist
            )

            direction = nav["dir"]
            distance = nav["distance"]
            degree = nav["deg"]

            self.log.write(f"dir: {direction}, dist: {distance}, deg: {degree}", "DEBUG")

            # 20m判定で終了
            if distance <= self.transition_dist:
                self.log.write("Finish GPS Phase", "INFO")
                self.motor.stop()
                break

            # GPS移動実行
            #self.motor.move(direction, 4.0, config.MOTOR_DUTY)
            ac_time=6 if direction =="forward" else 0.4
            self.motor.move(direction,ac_time,config.MOTOR_DUTY)
            if direction=="right" or direction=="left":
                if_dir="forward"
                self.motor.move(if_dir, 4 , 50 )
            previous_coordinate = current_coordinate
            time.sleep(config.SLEEP_TIME)

    def run_camera_phase(self):
        #self.log.write("Camera Phase Start", "INFO")
        
        while not self.stop_event.is_set():
            img = self.camera.cap()
            if img is None: continue

            self.log.write("Camera Phase Start","INFO")

            result = self.detector.dtc_img(img)
            self.log.write(f"Result: {result}", "INFO")

            if result == "goal":
                self.log.write("=== CanSat Finish ===", "INFO")
                hz=[523,587,659,698,783,880,987,1048]
                for num in hz:
                    self.buzzer.beep(0.5,num)
                    time.sleep(0.01)
                self.motor.stop()
                break
            
            elif result in ["left", "forward", "right"]:
                active_time = 2.0 if result == "forward" else 0.1
                if result=="right":
                    self.dtc_motor.dtc_move(mode=result, active_time=active_time, duty=40)
                elif result=="left":
                    self.dtc_motor.dtc_move(mode=result, active_time=0.2, duty=40)
                elif result=="forward":
                    self.dtc_motor.dtc_move(mode=result, active_time=active_time, duty=config.MOTOR_DUTY)


            elif result == "not find":
                self.log.write("Target Not Found", "WARNING")
                self.dtc_motor.dtc_move(mode="not find", active_time=0.1, duty=50)

            time.sleep(config.SLEEP_TIME)

    def cleanup(self):
        self.motor.cleanup()
        self.gps.disconnect()
        self.camera.end()
        self.log.write("Cleanup Complite", "INFO")

if __name__ == "__main__":
    controller = CanSatController()
    controller.run_mission()
