#75s
import WebGUI
import HAL
import Frequency
# Enter sequential code!

import cv2
i = 0
velocity = 10 #10
velocity_threshold = 150 #200
kp = 0.01 #0.012
kd = 0.03
ki = 0.0000
old_err = 0
total_err = 0
while True:
    img = HAL.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv,(0,125, 125), (30,255,255))
    

    contours, hierarchy = cv2.findContours(red_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(contours[0])
    if M["m00"] != 0:
        cX = M["m10"] / M["m00"]
        cY = M["m01"] / M["m00"]
    else:
        cX, cY = 0, 0

    if cX>0:
        err = 320 - cX
        #print(err)
        HAL.setV(velocity * max((1 - abs(err/ velocity_threshold)),0.0001))
        #HAL.setV(velocity)
        HAL.setW(kp * err + total_err*ki + kd * (err - old_err))
    if abs(err) > velocity_threshold:
        print(err)
    WebGUI.showImage(red_mask)
    #print('%d cX: %.2f cY: %.2f' % (i, cX, cY))
    i = i+1
    total_err += err
    old_err = err
        
    
    # Enter iterative code!
    Frequency.tick()
