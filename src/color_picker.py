import cv2
import csv
import os

CSV_FILE = "/home/pi/cansat_2026/log/hsv_date.csv"

numbers = [0.5,1,2,4,6,8,10,11,12,13,14,15,16,17,18,19,20]

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Image", "H", "S", "V"])

current_hsv = None
current_image_name = None

def mouse_event(event, x, y, flags, param):
    global current_hsv, current_image_name

    if event == cv2.EVENT_LBUTTONDOWN:
        h, s, v = current_hsv[y, x]

        print(f"\nHSV:{h},{s},{v}")
        user_input = input(">")

        try:
            h2, s2, v2 = map(int, user_input.split(","))
            with open(CSV_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([current_image_name, h2, s2, v2])
            print("保存しました")
        except:
            print("入力形式エラー（例: 5,40,40）")

for num in numbers:

    path = f"/home/pi/cansat_2026/img/2026_3_1_zyunkou/front/{num}fm.jpg"

    img = cv2.imread(path)
    if img is None:
        print(f"画像が見つかりません: {path}")
        continue

    current_image_name = f"{num}fm.jpg"
    current_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    print(f"\n--- {current_image_name} ---")
    print("クリックでHSV取得")
    print("qキーで次の画像へ")

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_event)
    cv2.imshow("Image", img)

    # qが押されるまで待機
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

print("全画像処理終了")
