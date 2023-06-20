import sys
from datetime import datetime

import cv2
import mss
import numpy as np
import psutil
import pyautogui

from resources import FolderPath


def process_running(process_name):
    """
    By Sanix darker
    Check if there is any running process that contains the given name
    processName.
    """

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (
                psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False


def screenshot(monitor_number=1):
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_number]
        # Grab the data
        ss = sct.grab(monitor)
        np_img = np.array(ss)
    return np_img


def screen_info():
    screen_width, screen_height = pyautogui.size()
    print(screen_width, screen_height)
    mouse_x, mouse_y = pyautogui.position()
    print(mouse_x, mouse_y)


def save_img(image, name="img", suffix="", folder_path=FolderPath.IMAGE):
    cur_time = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
    image_path = folder_path + name + suffix + cur_time + ".png"
    try:
        cv2.imwrite(image_path, image)
        return True
    except Exception as e:
        raise e.with_traceback(sys.exc_info()[2])


def show_img(img, window="", delay=0):
    cv2.imshow(winname=window, mat=img)
    cv2.waitKey(delay)
    cv2.destroyAllWindows()


def extract_object(image, show=False):
    """Extract object using HSV mask"""
    # threshold on white
    # Define lower and upper limits
    lower = np.array([0, 0, 0])
    upper = np.array([0, 0, 130])

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    if show:
        show_img(output)
    return output


def estimate_hsv(image):
    """Estimate HSV threshold of object to create extracted mask"""
    def nothing(x):
        pass

    # Create a window
    cv2.namedWindow('image')

    # create trackbars for color change
    cv2.createTrackbar('HMin', 'image', 0, 179,
                       nothing)  # Hue is from 0-179 for Opencv
    cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)

    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    output = image
    wait_time = 33

    while (1):

        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin', 'image')
        sMin = cv2.getTrackbarPos('SMin', 'image')
        vMin = cv2.getTrackbarPos('VMin', 'image')

        hMax = cv2.getTrackbarPos('HMax', 'image')
        sMax = cv2.getTrackbarPos('SMax', 'image')
        vMax = cv2.getTrackbarPos('VMax', 'image')

        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # Print if there is a change in HSV value
        if ((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (
                phMax != hMax) | (psMax != sMax) | (pvMax != vMax)):
            print(
                "(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
                    hMin, sMin, vMin, hMax, sMax, vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        # Display output image
        cv2.imshow('image', output)

        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
