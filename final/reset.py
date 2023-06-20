from datetime import datetime

import cv2
import numpy as np
import pyautogui

from resources import FolderPath
from symetry import superm2, draw


ss = pyautogui.screenshot()

# convert image to cv2 image object and show image shape
img_name = "SCR-20230616.jpeg"
ss_name = 'ss_' + datetime.now().strftime("%y%m%d_%H%M%S%f") + \
          '.png'
img = np.array(ss)
print(img.shape)


def crop_reset_captcha(ss):
    """crop the captcha image"""
    captcha = ss[785:1050, 1310:1570]
    captcha_image_name = FolderPath.IMAGE + \
                         ss_name.split(".")[0] + \
                         "-crop" + \
                         "." + ss_name.split(".")[1]

    cv2.imwrite(captcha_image_name, captcha)
    return captcha


# Calculate r, theta
def solve_reset_captcha(captcha_img):
    r, theta = superm2(captcha_img)
    # Draw symetry line
    sym_image = draw(captcha_img, r, theta)
    sym_image_name = FolderPath.IMAGE + ss_name.split(".")[0] + \
                     "-sym" + \
                     "." + \
                     ss_name.split(".")[1]

    if check_captcha_result():
        return True
    cv2.imwrite(sym_image_name, sym_image)
    cv2.imshow("symetry", sym_image)
    return False


def check_captcha_result():
    """TODO"""
    return True
