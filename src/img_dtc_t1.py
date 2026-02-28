import cv2
import numpy as np
#import time

low_color1=np.array([0,50,50]) # 赤色閾値1
hight_color1=np.array([5,255,255])
low_color2=np.array([170,50,50])# 赤色閾値2
hight_color2=np.array([180,255,255])

class Detect ():

    def __init__(self):
        self.cnt = 0

    def dtc_img(self,image):

        #img = cv2.imread(r"/home/pi/cansat_2026/img/9_17_zyunkou/20m_20250917_141312.jpg")#r"/home/pi/image/2.jpg"
        img=image

        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV) # RGB => YUV(YCbCr)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) # claheオブジェクトを生成
        img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0]) # 輝度にのみヒストグラム平坦化
        img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR) # YUV => RGB

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #RGBからHSV

        # mask生成
        bin_img1 = cv2.inRange(hsv, low_color1, hight_color1)
        bin_img2 = cv2.inRange(hsv, low_color2, hight_color2)
        mask = bin_img1 + bin_img2 # マスクを足し合わせる
        mask = cv2.medianBlur(mask, 5) #ノイズ処理
        masked_img = cv2.bitwise_and(img, img, mask= mask) # 元画像から特定の色を抽出

        # 輪郭を取得
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        area=cv2.contourArea(largest_contour)


        # その輪郭に外接矩形を描画
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(masked_img, (x, y), (x+w, y+h), (255, 20, 147), 1)
        #cv2.drawContours(masked_img,largest_contour,-1,(0,255,0),1)
        vertex=((x+w)+x)//2
        cv2.circle(masked_img,(vertex,y),5,(255,20,147),1)
        #print(((x+w)+x)/2)

        if area<550:
            #print("検出不可")
            path=r"/home/pi/cansat_2026/img/test_dtc/"#r"D:/program/2025_python/cansat_2026/img_dtc/"
            self.cnt+=1
            cv2.imwrite(path+str(self.cnt)+"_original.jpg",img)
            cv2.imwrite(path+str(self.cnt)+"_result.jpg",masked_img)
            return


        path=r"/home/pi/cansat_2026/img/test_dtc/"#r"D:/program/2025_python/cansat_2026/img_dtc/"

        self.cnt+=1

        cv2.imwrite(path+str(self.cnt)+"_original.jpg",img)
        cv2.imwrite(path+str(self.cnt)+"_result.jpg",masked_img)

        print("画像処理&保存完了")

        area_ratio=area/(1280*720)
        if area_ratio>0.7:
            return "end"

        if 0<vertex<426:
            return "left"
        elif 426<=vertex<853:
            return "forward"
        elif 853<=vertex<1280:
            return "right"

def main():
    detect_image=Detect()
    # while(True):
    #     detect_image.dtc_img()
    #     time.sleep(1)
    detect_image.dtc_img()

if __name__ == '__main__':
    main()