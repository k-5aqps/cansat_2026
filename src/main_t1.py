from typing import Dict
import time

from pyserial_t1 import (
    GPSModule,
    calculate_target_distance_angle,
)
from motor import MotorController

# ======================== ユーザー設定 ========================
# 目標座標（緯度・経度）: 実機に合わせて設定
GOAL_COORDINATE: Dict[str, float] = {
    "lat": 31.731920,  # 例: 霧島市周辺のダミー値。実際の目的地に置き換えてください
    "lon": 130.728022,
    #Latitude: 31.731798, Longitude: 130.727907
}

# 目標到達判定距離 [m]
TARGET_DISTANCE_M: float = 5.0

# モータ制御の基本設定
STEP_ACTIVE_TIME_S: float = 1.0   # 1ステップ動作時間
DUTY: int = 60                    # 0-100 の PWM デューティ
SLEEP_AFTER_STEP_S: float = 0.5   # ステップ間のインターバル

# GPS シリアル設定（必要に応じて変更）
GPS_PORT = "/dev/serial0"
GPS_BAUD = 9600
# ============================================================

def main() -> None:
    gps = GPSModule(port=GPS_PORT, baud_rate=GPS_BAUD)
    motor = MotorController()

    try:
        print("[INFO] Connecting GPS ...")
        gps.connect()
        print("[INFO] GPS connected. Fetching initial fixes...")

        # 初回: 前回座標(previous) と 現在座標(current) を用意
        # 有効な値が取れるまで数回リトライ
        def get_fix_with_retry(max_retry: int = 20, delay_s: float = 1.0):
            for _ in range(max_retry):
                lat, lon, satellites, utc_time, dop = gps.get_gps_data()
                if lat is not None and lon is not None:
                    return lat, lon
                time.sleep(delay_s)
            return None, None

        prev_lat, prev_lon = get_fix_with_retry()
        if prev_lat is None:
            raise RuntimeError("GPS の初期測位に失敗しました。")

        time.sleep(0.5)
        curr_lat, curr_lon = get_fix_with_retry()
        if curr_lat is None:
            raise RuntimeError("GPS の2回目測位に失敗しました。")

        previous_coordinate = {"lat": prev_lat, "lon": prev_lon}
        current_coordinate = {"lat": curr_lat, "lon": curr_lon}

        print(f"[READY] Start navigation -> Goal(lat={GOAL_COORDINATE['lat']:.6f}, lon={GOAL_COORDINATE['lon']:.6f})")

        while True:
            # 現在位置更新
            lat, lon, satellites, utc_time, dop = gps.get_gps_data()
            if lat is None or lon is None:
                print("[WARN] GPSデータ待機中...")
                time.sleep(0.5)
                continue

            previous_coordinate = current_coordinate
            current_coordinate = {"lat": lat, "lon": lon}

            # 進行方向と距離を計算
            result = calculate_target_distance_angle(
                current_coordinate,
                previous_coordinate,
                GOAL_COORDINATE,
                TARGET_DISTANCE_M,
            )

            direction = result.get("dir")
            degree = result.get("deg")
            distance = result.get("distance")

            print(f"[NAV] dist={distance:.2f} m, delta={degree:.1f} deg -> {direction}")

            if direction == "Immediate":
                print("[DONE] ゴール判定距離内に到達しました。停止します。")
                break

            # モータを1ステップ駆動（motor.move は内部で duty を設定して active_timeだけ駆動）
            if direction == "forward":
                motor.move("forward", STEP_ACTIVE_TIME_S, DUTY)
            elif direction == "left":
                motor.move("left", STEP_ACTIVE_TIME_S, DUTY) # 元はleft
            elif direction == "right":
                motor.move("right", STEP_ACTIVE_TIME_S, DUTY) # 元はright
            else:
                # 想定外の値は停止扱い
                motor.move("stop", STEP_ACTIVE_TIME_S, 0)

            time.sleep(SLEEP_AFTER_STEP_S)

    except KeyboardInterrupt:
        print("[INTERRUPT] 手動停止しました。")
    finally:
        try:
            gps.disconnect()
        except Exception:
            pass
        try:
            motor.cleanup()
        except Exception:
            pass
        print("[CLEANUP] リソースを解放しました。")


if __name__ == '__main__':
    main()