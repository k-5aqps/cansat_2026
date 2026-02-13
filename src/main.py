import time

from pyserial_t1 import GPSModule, calculate_target_distance_angle
from motor import MotorController
import logwrite


# ====== 設定 ======
GOAL_COORDINATE = {
    "lat": 35.000000,   # ←ここをゴール緯度に変更
    "lon": 135.000000   # ←ここをゴール経度に変更
}

TARGET_DISTANCE = 5  # 5m以内でゴール
DUTY = 40            # モーター出力
MOVE_TIME = 1        # 1回の動作時間（秒）


def main():

    log = logwrite.MyLogging()
    gps = GPSModule()
    motor = MotorController()

    previous_coordinate = None

    try:
        log.write("===== START AUTONOMOUS MODE =====", "INFO")

        gps.connect()

        while True:

            lat, lon, satellites, utc_time, dop = gps.get_gps_data()

            if lat is None or lon is None:
                log.write("GPS waiting...", "INFO")
                continue

            current_coordinate = {
                "lat": lat,
                "lon": lon
            }

            log.write(
                f"Current: lat={lat:.6f}, lon={lon:.6f}, sat={satellites}",
                "INFO"
            )

            # 初回は前進して向きを作る
            if previous_coordinate is None:
                motor.move("forward", MOVE_TIME, DUTY)
                previous_coordinate = current_coordinate
                continue

            # ゴール方向計算
            result = calculate_target_distance_angle(
                current_coordinate,
                previous_coordinate,
                GOAL_COORDINATE,
                TARGET_DISTANCE
            )

            direction = result["dir"]
            distance = result["distance"]
            degree = result["deg"]

            log.write(
                f"[NAV] dist={distance:.2f} m, deg={degree}, dir={direction}",
                "DEBUG"
            )

            # ゴール判定
            if direction == "Immediate":
                log.write("GOAL REACHED", "INFO")
                motor.stop()
                break

            # モーター制御
            motor.move(direction, MOVE_TIME, DUTY)

            # 前回座標更新
            previous_coordinate = current_coordinate

            time.sleep(0.2)

    except KeyboardInterrupt:
        log.write("Program stopped by user", "WARNING")

    except Exception as e:
        log.write(f"Error: {e}", "CRITICAL")

    finally:
        motor.cleanup()
        gps.disconnect()
        log.write("===== PROGRAM END =====", "INFO")


if __name__ == "__main__":
    main()