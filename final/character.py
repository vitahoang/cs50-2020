import time

from control import click
from menu import MenuChat
from resources import Map, ItemLoc
from text import extract_text_from
from utils import screenshot


class Character:
    class_name = ""
    character_name = ""
    current_loc = {}
    lvl: int
    reset: int
    point: int
    strength: int
    agility: int
    life: int
    energy: int

    def __init__(self):
        self.class_name = ""
        self.character_name = ""
        self.current_loc = {}
        self.lvl: int
        self.reset: int
        self.point: int
        self.strength: int
        self.agility: int
        self.life: int
        self.energy: int

    def cur_lvl(self):
        ss = screenshot()
        lvl_img = ss[28:65, 462:768]
        info = extract_text_from(lvl_img)
        info = [i for i in info.replace("\n", " ").split(" ") if i != ""]
        print(f"Level info: {info}")
        try:
            self.lvl = info[2]
            _char = {
                "character_name": info[0],
                "lvl": info[2]
            }
            return _char
        except:
            print("error " + str(IOError))
        return False

    def cur_loc(self):
        ss = screenshot()
        loc_img = ss[9:38, 2370:2610]
        info = extract_text_from(loc_img).replace("\n", "").split(" ")
        print(f"Map info: {info}")
        try:
            _map = {
                "map_name": info[0],
                "x": info[2],
                "y": info[3]
            }
            self.current_loc = _map
            return _map
        except:
            print("error " + str(IOError))
        return False

    def train(self, _map):
        print()
        if self.cur_lvl()["lvl"] == "600":
            print("Train Complete: Max LvL")
            return True
        MenuChat().move(_map)
        self.cur_loc()
        time.sleep(2)
        if self.current_loc["map_name"] == map:
            click(item_loc=ItemLoc.MV_LEFT)


character = Character()
character.train(Map.arena11)
