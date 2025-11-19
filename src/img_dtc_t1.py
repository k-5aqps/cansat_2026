import cv2
import numpy as np
#import time

low_color1=np.array([0,50,50]) # 赤色閾値1
hight_color1=np.array([5,255,255])
low_color2=np.array([170,50,50])# 赤色閾値2
hight_color2=np.array([180,255,255])

class detect ():

    def __init__(self):
        self.cnt = 0

    def dtc_img(self):

        img = cv2.imread(r"D:/program/2025_python/cansat_2026/img/9_17_zyunkou/2.0m_20250917_142113.jpg")#"/home/pi/image/2.jpg"

        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV) # RGB => YUV(YCbCr)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) # claheオブジェクトを生成
        img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0]) # 輝度にのみヒストグラム平坦化
        img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR) # YUV => RGB

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #RGBからHSV

        # mask生成
        bin_img1 = cv2.inRange(hsv, low_color1, hight_color1)
        bin_img2 = cv2.inRange(hsv, low_color2, hight_color2)
        mask = bin_img1 + bin_img2 # マスクを足し合わせる
        masked_img = cv2.bitwise_and(img, img, mask= mask) # 元画像から特定の色を抽出

        # 輪郭を取得
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # 面積が最大の輪郭を選ぶ
            largest_contour = max(contours, key=cv2.contourArea)

            # その輪郭に外接矩形を描画
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(masked_img, (x, y), (x+w, y+h), (0, 255, 0), 1)
            #cv2.drawContours(masked_img,largest_contour,-1,(0,255,0),1)
            cv2.circle(masked_img,(((x+w)+x)//2,y),5,(0,255,0),1)
            print(((x+w)+x)/2)
        else:
            print("検出不可")

        path=r"D:/program/2025_python/cansat_2026/img_dtc/"#"/home/pi/"

        self.cnt+=1

        cv2.imwrite(path+str(self.cnt)+"_original.jpg",img)
        cv2.imwrite(path+str(self.cnt)+"_result.jpg",masked_img)

        print("完了")

def main():
    detect_image=detect()
    # while(True):
    #     detect_image.dtc_img()
    #     time.sleep(1)
    detect_image.dtc_img()

if __name__ == '__main__':
    main()