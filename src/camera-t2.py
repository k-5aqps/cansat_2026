import picamera
import os

# 保存先のフォルダを指定
save_dir = "/home/pi/image"   # ここを保存したいフォルダに変更

# フォルダが存在しなければ作成
os.makedirs(save_dir, exist_ok=True)

# すでに保存されている写真から最大番号を調べて次の番号を決定
existing_files = [f for f in os.listdir(save_dir) if f.endswith(".jpg")]
numbers = []
for f in existing_files:
    try:
        numbers.append(int(os.path.splitext(f)[0]))  # "1.jpg" → 1
    except ValueError:
        pass

next_number = max(numbers) + 1 if numbers else 1

with picamera.PiCamera() as camera:
    #camera.resolution = (1024, 768)  # 解像度（必要に応じて変更）
    filename = os.path.join(save_dir, f"{next_number}.jpg")
    camera.capture(filename)
    print(f"{filename} に保存しました")