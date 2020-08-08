#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 14:35:58 2020

@author: gurkirpal
"""

'''
REFERECNCES:
   https://gogul.dev/software/hand-gesture-recognition-p1 
'''

#importing required libraries
import cv2
import keyboard as ky

#initialising variables
initial_background=None
height=480
width=640


#list to store location so as to where was the hand last time
l=[]
l.append('cen')


#function to detect the difference between initially detected background and current frame
def segment(image):
    global initial_background
    
    diff=cv2.absdiff(initial_background.astype("uint8"),image)    
    
    _,thresh=cv2.threshold(diff,25,255,cv2.THRESH_BINARY)
    cnt,_=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
    new=[]
    for contour in cnt:
        (x,y,w,h)=cv2.boundingRect(contour)
        
        #just to make it more smooth
        if(y+h>height/2):
            new.append(contour)

    if(len(new)==0):
        return
    
    else:
        segmented=max(new,key=cv2.contourArea)
        return (thresh,segmented)
    
cap=cv2.VideoCapture(0)

num_frames=0   #maintains frame count as we need to capture background till 50 frames
while True:
    ret,frame=cap.read()
    
    frame=cv2.flip(frame,1)   #flipping was required as my webcam was capturing the mirror image 
    #this may be commented out in some cases
    
    clone=frame.copy()
    gray = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    x=0
    y=0
    w=0
    h=0
    if(num_frames<50):
        
        #findind average
        if initial_background is None:
            initial_background=gray.copy().astype("float")
            continue
    
        cv2.accumulateWeighted(gray,initial_background,0.5)
    
    else:
        hand=segment(gray)
        
        if hand is not None:
            thresh,segmented=hand
            #cv2.imshow("thresh",thresh)    #uncomment this line to see the threshed image
            (x,y,w,h)=cv2.boundingRect(segmented)
            if(h>height//2):
                h=height//2;
            cv2.rectangle(clone,(x,y),(x+w,y+h),(0,255,0),2)    #remove this if you dont wish to 
            #see the contours 
            
            
    num_frames+=1
    
    #code from line 97 to has to be changed for games having different controls
    
    if((x+w/2)<width/2 and l[len(l)-1]!='left'):
        ky.press_and_release('w')     #'w' key is pressed 
        l.append('left')
        print('left')  #comment this if you dont want to print where your hand currently is
   
    
    if((x+w/2)>width/2 and l[len(l)-1]!='cen'):
        l.append('cen')
        print('cen')   #comment this if you dont want to print where your hand currently is
    

    cv2.imshow('my_window',clone)
    
    
    
    #close the program when 'esc' key is pressed
    if((cv2.waitKey(1) & 0xFF)==27):
        break

cap.release()
cv2.destroyAllWindows()
    
    
    
    
    
    
    
    
    