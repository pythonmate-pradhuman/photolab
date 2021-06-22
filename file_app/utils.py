
import numpy as np
import cv2
from PIL import Image

def get_filter(file,action):
    global res
    img=cv2.cvtColor(file,cv2.COLOR_BGR2RGB)
    if action=='FILTER':
      scale=70
      width=int(img.shape[0]*scale/100)
      height=int(img.shape[1]*scale/100)
      img1=cv2.resize(img, (width,height))
      img2 =cv2.imread('/media/file/pic25.png')
      
      img2=cv2.bitwise_not(img2)
      #print(img1.shape)
      #print(img2.shape)
      scale_fac=50
      w=img1.shape[0]
      h=img1.shape[1]

      x=0
      y=int(img1.shape[1] * scale_fac / 100)
      #crop image accor
      img3=img1[x:w,y:h]
      print('img3',img3.shape)
      #resize ref img 
      #img4=cv2.resize(img2, img3.shape[1::-1])
      img4=cv2.resize(img2, (img3.shape[0],img3.shape[1]))
      dst1 = cv2.bitwise_or(img3, img4)

      dst1[np.where((dst1==[255,255,255]).all(axis=2))]=[211,211,211]

      print(dst1.shape)
      #to place a pic at y
      rows,cols,channels = dst1.shape

      roi1 = dst1[0:rows,0:cols ]
      img1[0:w, y:y+cols]=roi1
      gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

      (thresh, blawh) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
      blur=cv2.GaussianBlur(blawh,(37,37),0)
      sum1=cv2.addWeighted(blur,0.3,gray,0.9,0)

      #providing effect
      img5=cv2.imread("back.jpg")
      img5=cv2.resize(img5, img1.shape[1::-1])
      gray1=cv2.cvtColor(img5,cv2.COLOR_BGR2GRAY)

      res=cv2.addWeighted(sum1,0.9,gray1,1,0)
      res=cv2.resize(res, img.shape[1::-1])

    return res
