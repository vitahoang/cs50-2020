import cv2
from rembg import remove

from control import click_item
from resources import ItemLoc, FolderPath
from symetry import superm2, draw
from transform import bg_remove_threshold, upscale
from utils import screenshot, save_img, show_img


def crop_reset_captcha(ss):
    """crop the captcha image"""
    captcha = ss[790:1070, 1320:1570]
    return captcha


# Calculate r, theta
def solve_captcha(save=True):
    r, theta = float, float
    captcha = None

    while theta != 0.0:
        captcha = cv2.imread(FolderPath.SAMPLE + "SCR-20230616.jpeg")
        show_img(captcha)
        captcha = crop_reset_captcha(captcha)
        show_img(captcha)
        captcha_scl = upscale(captcha)
        show_img(captcha_scl)
        captcha_obj = remove(captcha_scl)
        show_img(captcha_obj)
        r, theta = superm2(captcha_obj)
        print(r, theta)
        draw(captcha_scl, r, theta)
        show_img(captcha_scl)
        if theta == 0.0:
            click_item(loc=ItemLoc.RS_SEND)
        click_item(loc=ItemLoc.RS_RIGHT)
    draw(captcha, r, theta)
    show_img(captcha)
    # Draw symetry line
    if save:
        sym_image = draw(captcha, r, theta)
        save_img(image=sym_image, name="captcha", suffix="-sym")
    return True


def captcha_result():
    """TODO: check captcha result"""
    return True
