import sys

import cv2
import mss
import mss.tools
import numpy as np
import pyautogui

from control import open_app

IMAGE_FOLDER = "/Users/vitahoang/Code/cs50-2020/final/image/"

screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)
currentMouseX, currentMouseY = pyautogui.position()
print(currentMouseY, currentMouseY)


def screenshot(monitor_number: int):
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_number]
        # Grab the data
        ss = sct.grab(monitor)
        np_img = np.array(ss)
    return np_img


def main():
    if len(sys.argv) != 1:
        print("Usage: python main.py [monitor_number]")
        return -1

    # if you use multiple monitor, run "2" to capture the secondary monitor
    open_app()
    monitor_number = 1
    if len(sys.argv) > 1:
        monitor_number = int(sys.argv[1])
    image = screenshot(monitor_number)
    cv2.imshow("screenshot", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Check if image is loaded fine
    if image is None:
        print('Error loading image')
        return -1

    # extract edges object from the image
    dst = cv2.Canny(image, 50, 200, None, 3)


if __name__ == "__main__":
    main()
