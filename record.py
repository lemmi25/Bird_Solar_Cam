

import cv2 as cv
import numpy as np
from urllib.request import urlopen
import time
import requests
import os 

os.system('rm -r images')
os.system('mkdir images')
# create video 
# ffmpeg -framerate 10 -i test%d.jpg output.mp4

"""
Index   | Auflösung
13      | 1600 x 1200
12      | 1280 x 1024
11      | 1280 x 720
10      | 1024 x 768
9       | 800 x 600
8       | 640 x 480
7       | 480 x 320
6       | 400 x 296
5       | 320 x 240
4       | 240 x 240
3       | 240 x 176
2       | 176 x 144
1       | 160 x 120
0       | 96 x 96
"""

#change to your ESP32-CAM ip
# IP Adresse der ESP32-CAM
ipAdress = '192.168.0.56'
# Streaming Adresse aufbauen
requests.get('http://'+ipAdress+'/control?var=framesize&val=10')
url = 'http://' + ipAdress + ':81/stream'
CAMERA_BUFFRER_SIZE=4096
stream=urlopen(url)
bts=b''
i = 0

while True:    
    try:
        bts+=stream.read(CAMERA_BUFFRER_SIZE)
        jpghead=bts.find(b'\xff\xd8')
        jpgend=bts.find(b'\xff\xd9')
        if jpghead>-1 and jpgend>-1:
            jpg=bts[jpghead:jpgend+2]
            bts=bts[jpgend+2:]
            img=cv.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv.IMREAD_UNCHANGED)
            
            img=cv.resize(img,(1024,768))
            cv.imwrite("images/test" + str(i) + ".jpg",img)
            time.sleep(0.05)
            print('Take Image: ' + str(i))
            i += 1
            #cv.imshow("a",img)
        if cv.waitKey(1) & 0xFF == ord('a'):
            break
    except Exception as e:
        print("Error:" + str(e))
        bts=b''
        stream=urlopen(url)
        continue

# After we release our webcam, we also release the output
cv.destroyAllWindows()
