import time

import cv2
import pyautogui
import pyscreeze

from models.resources import Screen, FolderPath
from utils import screenshot, click, _raise, show_img

START = {
    "name": "start",
    "img_path": "start.png",
    "screen": Screen.START,
    "loc": {"x": 1175, "y": 769},
    "region": (1294, 1662, 2138, 2560)
}

VIP = {
    "name": "vip",
    "img_path": "vip.png",
    "screen": Screen.SERVER,
    "loc": {"x": 720, "y": 428},
    "region": (798, 1008, 1312, 1576)
}

SPOT = {
    "name": "spot",
    "img_path": "spot.png",
    "screen": Screen.SERVER,
    "loc": {"x": 724, "y": 450},
    "region": (798, 1008, 1312, 1576)
}

SPOT5 = {
    "name": "spot5",
    "img_path": "spot5.png",
    "screen": Screen.SERVER,
    "loc": {"x": 724, "y": 450},
    "region": (798, 1008, 1312, 1576)
}
VIP5 = {
    "name": "vip5",
    "img_path": "vip5.png",
    "screen": Screen.SERVER,
    "loc": {"x": 724, "y": 450},
    "region": (798, 1008, 1312, 1576)
}
C_MAGIC = {
    "name": "c_magic",
    "img_path": "c-magic.png",
    "screen": Screen.CHARACTER,
    "loc": {"x": 1037, "y": 556},
    "region": (562, 1474, 1804, 2366)
}
C_SOUL = {
    "name": "c_soul",
    "img_path": "c-soul.png",
    "screen": Screen.CHARACTER,
    "loc": {"x": 724, "y": 450},
    "region": (562, 1474, 1804, 2366)
}
C_ENTER = {
    "name": "c_enter",
    "img_path": "c-enter.png",
    "screen": Screen.CHARACTER,
    "loc": {"x": 724, "y": 450},
    "region": (1476, 1656, 1134, 1764)
}
CHAT_SEND = {
    "name": "chat_send",
    "img_path": "chat-send.png",
    "screen": Screen.IN_GAME,
    "loc": {"x": 724, "y": 450},
    "region": (32, 110, 2352, 2548)
}

INVENTORY_SLOT = {
    "name": "inventory_slot",
    "img_path": "inventory-slot.png",
    "screen": Screen.IN_GAME,
    "loc": {"x": 1005, "y": 473},
    "region": (910, 1472, 1968, 2530)
}


class Item:
    name: str
    img_path: str
    screen: str
    loc: {}
    region: ()

    def __init__(self, item):
        self.name = item["name"]
        self.img_path = item["img_path"]
        self.screen = item["screen"]
        self.loc = item["loc"]
        self.region = item["region"]

    def find_item(self, item_path: str = None, region: tuple = None,
                  preview=False):
        """find item given an image then return its central location on
        screen"""
        path = FolderPath.ITEM + \
               self.img_path if not item_path else item_path
        print(f"Finding: {path}")
        target_region = self.region if not region else region
        result = None
        for _ in range(3):
            time.sleep(3)
            query_img = cv2.imread(path)
            target_img = screenshot(region=target_region)
            if preview:
                show_img(query_img)
                show_img(target_img)
            result = pyscreeze.locate(needleImage=query_img,
                                      haystackImage=target_img,
                                      grayscale=False,
                                      confidence=0.7)
            if result:
                break
        if result is None:
            print("Item not found")
            return False
        loc_x, loc_y = pyautogui.center(result)
        loc_x += target_region[2]
        loc_y += target_region[0]
        print(loc_x / 2, loc_y / 2)
        return {"x": loc_x / 2, "y": loc_y / 2}

    def click_item(self, find=True, pick_up=False):
        try:
            if not find:
                click(_loc=self.loc)
                if pick_up:
                    click(_loc=self.loc)
                return self.loc
            loc = self.find_item()
            click(_loc=loc)
            return loc
        except Exception as e:
            _raise(e)
