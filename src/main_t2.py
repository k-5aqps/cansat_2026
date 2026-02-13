import time

from pyserial_t1 import (
    GPSModule,
    calculate_target_distance_angle,
    cheak_data
)
from motor import MotorController
from logwrite import MyLogging


# ===== 設定値 =====
TARGET_DISTANCE = 5        # ゴール判定距離（m）
MOVE_TIME = 1.5            # モーターを動かす時間（秒）
DUTY = 50                  # PWMデューティ比

GOAL_COORDINATE = {
    "lat": 31.731985,      # ← ゴール緯度（要変更）
    "lon": 130.727790      # ← ゴール経度（要変更）
#Latitude: 31.731985, Longitude: 130.727790
}
# ==================


def gps_phase():
    log = MyLogging()
    gps = GPSModule()
    motor = MotorController()

    previous_coordinate = None

    try:
        log.write("GPS phase start", "INFO")
        gps.connect()
        log.write("GPS connected", "INFO")

        while True:
            lat, lon, satellites, utc_time, dop = gps.get_gps_data()

            if lat is None or lon is None:
                log.write("GPS retrieving data", "WARNING")
                continue

            current_coordinate = {"lat": lat, "lon": lon}

            log.write(f"lat={lat:.6f}, lon={lon:.6f}, sat={satellites}, dop={dop}","INFO")
            log.forCSV(lat,lon)

            # 初回は比較用データがないので保存のみ
            if previous_coordinate is None:
                previous_coordinate = current_coordinate
                log.write("初回GPS取得、移動判定スキップ", "DEBUG")
                continue

            # データ妥当性チェック
            # if not cheak_data(lat, lon, previous_coordinate):
            #     log.write("GPSデータ異常のためスキップ", "WARNING")
            #     continue

            # 進行方向・距離計算
            result = calculate_target_distance_angle(
                current_coordinate,
                previous_coordinate,
                GOAL_COORDINATE,
                TARGET_DISTANCE
            )

            log.write(
                f"判定 dir={result['dir']}, deg={result['deg']}, distance={result['distance']:.2f}m",
                "INFO"
            )

            # ゴール判定
            if result["dir"] == "Immediate":
                log.write("Finished", "INFO")
                motor.move("stop", 0, 0)
                break

            # モーター制御
            if result["dir"] in ["forward", "left", "right"]:
                log.write(f"モーター動作: {result['dir']}", "DEBUG")
                motor.move(result["dir"], MOVE_TIME, DUTY)

            previous_coordinate = current_coordinate
            time.sleep(0.5)

    except KeyboardInterrupt:
        log.write("GPSフェーズ中断（KeyboardInterrupt）", "WARNING")
    except Exception as e:
        log.write(f"GPSフェーズ異常終了: {e}", "CRITICAL")
    finally:
        gps.disconnect()
        motor.cleanup()
        log.write("GPSフェーズ終了", "INFO")


if __name__ == "__main__":
    gps_phase()
