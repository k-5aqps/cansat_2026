from buzzer import BUZZER
import time

buzzer = BUZZER()

def main():
    # 音階を鳴らす
    hz = [1048, 987, 880, 783, 698, 659, 587, 523]

    for num in hz:
        buzzer.beep(0.5, num)
        time.sleep(0.05)

    print("next")
    time.sleep(5)

    #    self.stop_event.set()

    # 1048Hzを5回鳴らす
    cnt = 0
    while cnt < 5:
        buzzer.beep(0.5, 1048)   # ← ここを修正
        time.sleep(0.05)
        cnt += 1

if __name__ =='__main__':
    main()