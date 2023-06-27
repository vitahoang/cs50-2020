from control import solve_captcha
from models.item import *
from models.resources import ItemLoc

click(_loc=ItemLoc.INVENTORY)
box = Item(INVENTORY_SLOT)
box.click_item(find=False, pick_up=True)
box.click_item()
click(_loc=ItemLoc.INVENTORY)

solve_captcha()
