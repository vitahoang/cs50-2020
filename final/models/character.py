import re

from models.resources import ItemLoc
from models.text import extract_text_from
from utils import screenshot, _raise, click


class Character:
    class_name = ""
    character_name = ""
    current_loc = {}
    lvl: int
    reset: int
    total_point: int
    free_point: int
    added_point: int
    RESET_POINTS = 11381
    INIT_POINTS = 26
    MAX_POINTS = 32767
    strength: int
    agility: int
    life: int
    energy: int

    def __init__(self):
        self.class_name = ""
        self.character_name = ""
        self.current_loc = {}

    def cur_lvl(self):
        click(item_loc=ItemLoc.STAT_MENU)
        ss = screenshot()
        stat_img = ss[450:490, 1430:1906]
        info = extract_text_from(stat_img)
        print(info)
        info = [i for i in info.replace("\n", " ").split(" ") if i != ""]
        print(f"Level info: {info}")
        if len(info) < 2:
            print("LvL [info] has less than 2 elements")
            return False
        try:
            self.lvl = int(info[1])
            self.free_point = 0
            _char = {
                "lvl": int(info[1]),
                "free_point": 0,
            }
            if len(info) == 4:
                self.free_point = info[3]
                _char["free_point"] = info[3]

            click(item_loc=ItemLoc.STAT_MENU)
            print(_char)
            return _char
        except Exception as e:
            _raise(e)
        click(item_loc=ItemLoc.STAT_MENU)
        return False

    def cur_stat(self):
        click(item_loc=ItemLoc.STAT_MENU)
        ss = screenshot()
        stat_img = ss[550:1290, 1430:1950]
        info = extract_text_from(stat_img).replace(" ", "")
        _regex = re.compile(r'^[a-zA-Z]{1,8}:(\d+)\n', re.MULTILINE)
        info = re.findall(_regex, info)
        print(f"Stat info: {info}")
        if len(info) < 4:
            print(f"Stat [info] only has {len(info)} element(s)")
            return False
        try:
            stat = {
                "strength": int(info[0]),
                "agility": int(info[1]),
                "life": int(info[2]),
                "energy": int(info[3])
            }

            print(f"Stat info: {stat}")
            self.strength = stat["strength"]
            self.agility = stat["agility"]
            self.life = stat["life"]
            self.energy = stat["energy"]
            self.added_point = stat["strength"] + \
                               stat["agility"] + \
                               stat["life"] + \
                               stat["energy"]
            click(item_loc=ItemLoc.STAT_MENU)
            return stat
        except Exception as e:
            click(item_loc=ItemLoc.STAT_MENU)
            _raise(e)
        return False

    def cur_reset(self):
        try:
            self.cur_lvl()
            self.cur_stat()
            self.total_point = self.free_point + self.added_point
            self.reset = (self.total_point - self.INIT_POINTS) \
                         % self.RESET_POINTS
            if self.reset > 10:
                self.reset = 0
            print(f"Reset: {self.reset}; Free Points: {self.free_point}")
            return self.reset
        except Exception as e:
            _raise(e)

    def cur_loc(self):
        ss = screenshot()
        loc_img = ss[10:64, 2256:2640]
        info = extract_text_from(loc_img).replace("\n", "").split(" ")
        print(f"Map info: {info}")
        if len(info) !=4:
            print("Location [info] has less than 4 elements")
            return False
        try:
            _map = {
                "map_name": info[0],
                "x": info[2],
                "y": info[3]
            }
            self.current_loc = _map
            return _map
        except Exception as e:
            _raise(e)
        return False

    @staticmethod
    def check_max_lvl():
        ss = screenshot()
        message = ss[1495:1545, 845:1495]
        alert = extract_text_from(message).replace("\n", "")
        print(alert)
        if alert == "You have reached a maximum level":
            print("Train Complete: Max LvL")
            return True
        return False
