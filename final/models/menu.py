import time

import pyautogui

from utils import _raise, click


class Menu:
    _menu = None
    lv1 = None
    lv2 = None
    lv3 = None

    def open(self):
        click(self._menu)

    @staticmethod
    def open_menu(menu_lvl: str, menu_name: str):
        try:
            click(eval("self." + menu_lvl + "[" + menu_name + "]"))
            return True
        except Exception as e:
            _raise(e)
        return False

    def open_menu_lv1(self, map_name: str):
        pyautogui.moveTo(self.lv1[map_name]["x"],
                         self.lv1[map_name]["y"])
        pyautogui.click()

    def open_menu_lv2(self, map_name: str):
        pyautogui.moveTo(self.lv2[map_name]["x"],
                         self.lv2[map_name]["y"])
        pyautogui.click()


class MenuMap(Menu):
    _menu = {"x": 1290, "y": 241}
    lv1 = {
        "arena": {"x": 866, "y": 423},
        "lorencia": {"x": 590, "y": 388},
        "noria": {"x": 590, "y": 423}
    }
    lv2 = {
        "lorencia": {"x": 590, "y": 395},
        "noria": {"x": 592, "y": 427},
        "NPCMR": {"x": 592, "y": 461},
        "NPCPK": {"x": 725, "y": 366},
        "arena11": {"x": 725, "y": 520},
        "arena9": {"x": 851, "y": 481}
    }

    def map_arena(self, map_name: str):
        time.sleep(1)
        self.open()
        time.sleep(1)
        self.open_menu_lv1("arena")
        self.open_menu_lv2(map_name)
        time.sleep(1)

    def map_lorencia(self, map_name: str):
        time.sleep(1)
        self.open()
        time.sleep(1)
        self.open_menu_lv1("lorencia")
        self.open_menu_lv2(map_name)
        time.sleep(1)

    def map_noria(self, map_name: str):
        time.sleep(1)
        self.open()
        time.sleep(1)
        self.open_menu_lv1("noria")
        self.open_menu_lv2(map_name)
        time.sleep(1)


class MenuSetting(Menu):
    pass
