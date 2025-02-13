import cv2
import numpy as np
from tracker import*
import cvzone

cap=cv2.VideoCapture('newCam1.avi')
lower_range=np.array([0,0,150])
upper_range=np.array([179,255,255])

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        point = [x, y]
        # print(point)
  
        
tracker=Tracker()
# cv2.namedWindow('RGB')
# cv2.setMouseCallback('RGB', RGB)
area=[(55,200),(570,200),(570,250),(55,250)]
counter=[]
while True:
    ret,frame=cap.read()
    if not ret:
        break
    frame=cv2.resize(frame,(640,480))
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_range,upper_range)
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    list=[]
    for c in cnts:
        x=4000
        if cv2.contourArea(c)>x and cv2.contourArea(c)<=13000:
            x,y,w,h=cv2.boundingRect(c)
            list.append([x,y,w,h])
    bbox_idx=tracker.update(list)
    for bbox in bbox_idx:
        x1,y1,w1,h1,id=bbox
        cx=int(x1+x1+w1)//2
        cy=int(y1+y1+h1)//2
            
        results=cv2.pointPolygonTest(np.array(area,np.int32),((cx,cy)),False)
        if results>=0:
            cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
            cv2.rectangle(frame,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
            # cvzone.putTextRect(frame,f"{id}",(x1,y1),2,2)
            if counter.count(id)==0:
                counter.append(id)
    cv2.polylines(frame,[np.array(area,np.int32)],True,(0,0,255),2)
    c1=(len(counter)) 
    # print(counter)
    cvzone.putTextRect(frame,f" TOTAL COUNT = {c1}",(50,60),thickness=3, offset=10,colorR=(255, 100, 0))
    
    cv2.imshow("Counter",frame)
    cv2.imshow("Mask",mask)
    if cv2.waitKey(25) & 0xFF == ord("q"): 
        break
    
cap.release()
cv2.destroyAllWindows()
