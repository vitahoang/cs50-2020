from control import click_item
from resources import ItemLoc
from symetry import superm2, draw
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
        captcha = crop_reset_captcha(screenshot())
        # estimate_hsv(captcha)
        # captcha_obj = extract_object(captcha, show=True)
        r, theta = superm2(captcha)
        print(r, theta)
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
    """TODO"""
    return True
