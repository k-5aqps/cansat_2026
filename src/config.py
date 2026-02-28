# ===== ゴール設定 =====
GOAL_LAT = 31.731872      # ←変更
GOAL_LON = 130.727958     # ←変更
#Latitude: 31.731872, Longitude: 130.727958, Satellites: 9, Time: 055507, DOP: 0.96 INFO
TARGET_DISTANCE = 5       # ゴール判定距離[m]


# ===== モーター設定 =====
MOTOR_DUTY = 70           # 出力(0-100)
#MOVE_TIME = 2.0           # 1回の動作時間[秒]
SLEEP_TIME = 0.2          # ループ間待機時間


# ===== GPS設定 =====
#GPS_PORT = "/dev/serial0"
#GPS_BAUDRATE = 9600


# ===== 安全制御 =====
MIN_SATELLITES = 4        # 最低衛星数
MAX_DOP = 3.0             # DOP許容値