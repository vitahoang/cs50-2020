import re
import time

from models.resources import Point, ItemLoc
from models.text import extract_text_from
from utils import screenshot, _raise, click, chat


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

    def cur_lvl(self, menu=True):
        if menu:
            click(item_loc=ItemLoc.STAT_MENU)
        ss = screenshot()
        stat_img = ss[450:490, 1430:1906]
        info = extract_text_from(stat_img)
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
                self.free_point = int(info[3])
                _char["free_point"] = info[3]
            if menu:
                click(item_loc=ItemLoc.STAT_MENU)
            return _char
        except Exception as e:
            _raise(e)
        if menu:
            click(item_loc=ItemLoc.STAT_MENU)
        return False

    def cur_stat(self):
        click(item_loc=ItemLoc.STAT_MENU)
        if not self.cur_lvl(menu=False):
            return False
        ss = screenshot()
        stat_img = ss[550:1290, 1430:1950]
        info = extract_text_from(stat_img).replace(" ", "")
        _regex = re.compile(r'^[a-zA-Z]{1,8}:(\d+)\n', re.MULTILINE)
        info = re.findall(_regex, info)
        info = [int(i) for i in info]
        print(f"Stat info: {info}")
        if len(info) < 4:
            print(f"Stat [info] only has {len(info)} element(s)")
            return False
        try:
            stat = {
                "strength": info[0],
                "agility": info[1],
                "life": info[2],
                "energy": info[3]
            }

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
            self.cur_stat()
            if not self.added_point:
                return False
            self.total_point = self.free_point + self.added_point
            self.reset = (self.total_point - self.INIT_POINTS) \
                         // self.RESET_POINTS
            if self.total_point == (10193 + self.INIT_POINTS):
                self.reset = 1
            print(f"Reset: {self.reset}; Free Points: {self.free_point}")
            return self.reset
        except Exception as e:
            _raise(e)

    def cur_loc(self):
        time.sleep(1)
        ss = screenshot()
        loc_img = ss[10:64, 2290:2640]
        info = []
        for _ in range(3):
            info = extract_text_from(loc_img).replace("\n", "").split(" ")
            if info:
                print(f"Map info: {info}")
                break
            time.sleep(1)
        if len(info) < 4:
            print("Location [info] has less than 4 elements")
            _map = {
                "map_name": info[0],
                "x": None,
                "y": None
            }
            return info
        try:
            _map = {
                "map_name": info[0],
                "x": info[2],
                "y": info[3]
            }
            self.current_loc = _map
            return info
        except Exception as e:
            _raise(e)
        return None

    @staticmethod
    def check_max_lvl():
        ss = screenshot()
        message = ss[1500:1645, 800:1495]
        alert = extract_text_from(message).replace("\n", "")
        print(alert)
        if re.search("You have reached a maximum level", alert):
            print("Train Complete: Max LvL")
            return True
        return False

    def add_point(self, stat: str):
        if self.free_point == 0:
            print("No free point to add")
            return False
        p_max = self.MAX_POINTS
        p_free = self.free_point
        cur_p_stat = eval("self." + Point().look_up_by_val(stat).lower())

        if cur_p_stat < p_max:
            if (p_max - cur_p_stat) > p_free:
                add_p = p_free
                chat(stat, str(add_p))
                return True
            add_p = p_max - cur_p_stat
            chat(stat, str(add_p))
            self.free_point = p_free - add_p
        return False

    def check_max_reset(self):
        self.cur_reset()
        try:
            if self.lvl < 600:
                return False
            if self.added_point == self.MAX_POINTS * 4:
                print("Max reset!")
                return True
        except Exception as e:
            _raise(e)

    def add_all_point(self):
        while not self.check_max_reset() and self.free_point != 0:
            if self.add_point(Point.AGILITY):
                break
            if self.add_point(Point.ENERGY):
                break
            if self.add_point(Point.STRENGTH):
                break
            if self.add_point(Point.LIFE):
                break
        return True
