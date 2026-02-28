import time

from pyserial_t1 import GPSModule, calculate_target_distance_angle
from motor_t1 import MotorController
import logwrite
import config


def main():

    log = logwrite.MyLogging()

    # ===== configから読み込み =====
    GOAL_COORDINATE = {
        "lat": config.GOAL_LAT,
        "lon": config.GOAL_LON
    }

    TARGET_DISTANCE = config.TARGET_DISTANCE
    DUTY = config.MOTOR_DUTY
    MOVE_TIME = 2.0
    SLEEP_TIME = config.SLEEP_TIME

    gps = GPSModule()  # 将来GPS_PORT使うならここに指定
    motor = MotorController()

    previous_coordinate = None

    try:
        log.write("GPS phase start", "INFO")
        gps.connect()
        log.write("GPS connected", "INFO")

        while True:

            lat, lon, satellites, utc_time, dop = gps.get_gps_data()

            if lat is None or lon is None:
                log.write("GPS waiting...", "INFO")
                continue

            # 安全制御（config反映）
            if satellites is not None and satellites < config.MIN_SATELLITES:
                log.write("Satellite不足", "WARNING")
                continue

            current_coordinate = {
                "lat": lat,
                "lon": lon
            }

            log.write(
                f"Current: lat={lat:.6f}, lon={lon:.6f}, sat={satellites}, dop={dop}",
                "INFO"
            )
            log.forCSV(lat, lon)

            if previous_coordinate is None:
                motor.move("forward", 5, 70)
                previous_coordinate = current_coordinate
                continue

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
                f"dir={direction},[NAV] dist={distance:.2f} m, deg={degree}",
                "DEBUG"
            )

            if direction == "Immediate":
                log.write("GOAL REACHED", "INFO")
                motor.stop()
                break

            motor.move(direction, MOVE_TIME, DUTY)

            previous_coordinate = current_coordinate

            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        log.write("Program stopped by user", "WARNING")

    except Exception as e:
        log.write(f"GPSフェーズ異常終了: {e}", "CRITICAL")

    finally:
        motor.cleanup()
        gps.disconnect()
        log.write("GPSフェーズ終了", "INFO")


if __name__ == "__main__":
    main()