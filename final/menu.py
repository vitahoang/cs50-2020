import json
import time

import pyautogui

with open("menu.json", "r") as file:
    menu = json.load(file)


class Menu:
    _menu = menu
    _lv1 = None
    _lv2 = None

    def __int__(self):
        pass

    def open_menu(self):
        pyautogui.moveTo(self._menu["x"], self._menu["y"])
        pyautogui.click()

    def open_menu_lv1(self, map_name: str):
        pyautogui.moveTo(self._lv1[map_name]["x"],
                         self._lv1[map_name]["y"])
        pyautogui.click()

    def open_menu_lv2(self, map_name: str):
        pyautogui.moveTo(self._lv2[map_name]["x"],
                         self._lv2[map_name]["y"])
        pyautogui.click()


class MenuMap(Menu):
    _menu = {"x": 1290, "y": 241}
    _lv1 = {
        "arena": {"x": 866, "y": 423},
        "lorencia": {"x": 590, "y": 388},
        "noria": {"x": 590, "y": 423}
    }
    _lv2 = {
        "lorencia": {"x": 590, "y": 395},
        "noria": {"x": 592, "y": 427},
        "NPCMR": {"x": 592, "y": 461},
        "arena_npc": {"x": 725, "y": 366},
        "arena_11": {"x": 725, "y": 520},
        "arena_9": {"x": 851, "y": 481}
    }

    def map_arena(self, map_name: str):
        time.sleep(1)
        self.open_menu()
        time.sleep(1)
        self.open_menu_lv1("arena")
        self.open_menu_lv2(map_name)
        time.sleep(1)

    def map_lorencia(self, map_name: str):
        time.sleep(1)
        self.open_menu()
        time.sleep(1)
        self.open_menu_lv1("lorencia")
        self.open_menu_lv2(map_name)
        time.sleep(1)

    def map_noria(self, map_name: str):
        time.sleep(1)
        self.open_menu()
        time.sleep(1)
        self.open_menu_lv1("noria")
        self.open_menu_lv2(map_name)
        time.sleep(1)


class MenuChat(Menu):
    _menu = {"x": 1027, "y": 825}

    def chat(self, message):
        print(message)
        self.open_menu()
        time.sleep(2)
        chars = [i for i in message]
        pyautogui.write(chars)
        pyautogui.press("enter")

    def add(self, point_type: str, point: int):
        self.chat(point_type + str(point))
