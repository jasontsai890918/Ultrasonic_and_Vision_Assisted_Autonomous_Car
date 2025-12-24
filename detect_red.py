import cv2
import numpy as np
#create a VideoCapture object
cap = cv2.VideoCapture(0)
red_lower = np.array([0,43,46])
red_upper = np.array([10,255,255])
blue_lower = np.array([100,43,46])
blue_upper = np.array([124,255,255])
green_lower=np.array([35,43,46])
green_upper=np.array([77,255,255])
yellow_lower=np.array([26,43,46])
yellow_upper=np.array([34,255,255])
cap.set(3,320)
cap.set(4,240)
def get_red():

    # Capture Video from Camera
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask_blue = cv2.inRange(hsv, blue_upper, blue_upper)
    # Threshold the HSV image to get only green colors
    mask_green = cv2.inRange(hsv, green_lower, green_upper)
    # Threshold the HSV image to get only red colors   
    mask_red = cv2.inRange(hsv, red_lower, red_upper)
    # Bitwise-AND mask and original image

    mask_blue = cv2.GaussianBlur(mask_blue, (3, 3), 0)
    mask_green = cv2.GaussianBlur(mask_green, (3, 3), 0) 
    mask_red = cv2.GaussianBlur(mask_red, (3, 3), 0)

    res_blue = cv2.bitwise_and(frame,frame, mask= mask_blue)
    res_green = cv2.bitwise_and(frame,frame, mask= mask_green)
    res_red = cv2.bitwise_and(frame,frame, mask= mask_red)

    red_blur = cv2.medianBlur(mask_red, 7)
    blue_blur = cv2.medianBlur(mask_blue, 7)
    green_blur = cv2.medianBlur(mask_green, 7)

    red_color = np.max(red_blur)
    blue_color = np.max(blue_blur)
    green_color = np.max(green_blur)

    print("red: ",red_color)
    print("blue: ",blue_color)
    print("green: ",green_color)

    cv2.imshow('frame',frame)
    cv2.imshow('mask_blue)',mask_blue)
    cv2.imshow('mask_green',mask_green)
    cv2.imshow('mask_red',mask_red)
    return red_color

def finish():
    cv2.destroyAllWindows()