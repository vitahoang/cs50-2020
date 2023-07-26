import re
import time

from models.resources import Point, ItemLoc
from models.text import extract_text_from
from utils import screenshot, _raise, click, chat, show_img


class Character:
    """
    Represents a game character with attributes such as level, stats,
    and location.
     Attributes:
        class_name (str): The class of the character.
        character_name (str): The name of the character.
        current_loc (dict): The current location of the character.
        lvl (int): The level of the character.
        reset (int): The reset count of the character.
        total_point (int): The total points of the character.
        free_point (int): The free points of the character.
        added_point (int): The added points of the character.
        strength (int): The strength of the character.
        agility (int): The agility of the character.
        life (int): The life of the character.
        energy (int): The energy of the character.
     Methods:
        cur_lvl(menu=True): Updates the level and free points of the character.
        cur_stat(): Updates the stats of the character.
        cur_reset(): Updates the reset count of the character.
        cur_loc(): Updates the location of the character.
        check_max_lvl(): Checks if the character has reached the maximum level.
        add_point(stat): Adds free points to the specified stat.
        check_max_reset(): Checks if the character has reached the maximum reset count.
        add_all_point(): Adds all free points to the character's stats.
    """
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
        self.max_reset = False
        self.class_name = ""
        self.character_name = ""
        self.current_loc = {}
        self.added_point = 0
        self.lvl = 0

    def cur_lvl(self, menu=True):
        """
        Update the character's level and free points based on a screenshot
        of the game's status menu.
        """

        # If menu is True, click on the STAT_MENU item
        print(">>>Func: cur_lvl")
        if menu:
            click(_loc=ItemLoc.STAT_MENU)
        # Take a screenshot and extract the level information
        ss = screenshot()
        stat_img = ss[450:490, 1430:1906]
        info = extract_text_from(stat_img)
        info = [i for i in info.replace("\n", " ").split(" ") if i != ""]
        print(f"Level info: {info}")
        # If the information has less than 2 elements, return False
        if len(info) < 2:
            print("LvL [info] has less than 2 elements")
            return False
        if len(info) > 4:
            print("LvL [info] has more than 4 elements")

        # Try to extract the level and free point information
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
                click(_loc=ItemLoc.STAT_MENU)
            return _char
        except Exception as e:
            _raise(e)
        if menu:
            click(_loc=ItemLoc.STAT_MENU)
        return False

    def cur_stat(self, menu=True):
        """
        Update the character's stats (strength, agility, life, and energy)
        based on a screenshot of the game's status menu.
        """
        print(">>>Func: cur_stat")
        if menu:
            click(_loc=ItemLoc.STAT_MENU)
        if not self.cur_lvl(menu=False):
            return False
        ss = screenshot()
        stat_img = ss[550:1290, 1430:1800]
        info = extract_text_from(stat_img) \
            .replace(" ", "") \
            .replace("—", "") \
            .replace("&", "")
        _regex = re.compile(r'^[a-zA-Z]{1,8}:(\d{1,5})$', re.MULTILINE)
        info = re.findall(_regex, info)
        info = [int(i) for i in info]
        print(f"Stat info: {info}")
        if len(info) < 4:
            print(f"Stat [info] only has {len(info)} element(s)")
            if menu:
                click(_loc=ItemLoc.STAT_MENU)
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
            if menu:
                click(_loc=ItemLoc.STAT_MENU)
            return stat
        except Exception as e:
            if menu:
                click(_loc=ItemLoc.STAT_MENU)
            _raise(e)
        return False

    def cur_reset(self):
        """
        Update the character's reset count based on the current stats and
        free points.
        """
        print(">>>Func: cur_reset")
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
            self.check_max_reset()
            return self.reset
        except Exception as e:
            _raise(e)

    def cur_loc(self):
        """
        Update the character's current location based on a screenshot of
        the game's location information.
        """
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
        """
        Check if the character has reached the maximum level based on a screenshot of the game's message alert.
        """
        ss = screenshot()
        message = ss[1500:1645, 800:1495]
        alert = extract_text_from(message).replace("\n", "")
        if re.search("maximum level", alert):
            print("Train Complete: Max LvL")
            return True
        return False

    def add_point(self, stat: str, p: int = None):
        """
        Add free points to the specified stat if possible, up to the
        maximum allowed points.
        """
        print(f"Func: add_point {stat}")
        if self.free_point == 0:
            print("No free point to add")
            return False
        p_max = self.MAX_POINTS
        p_free = self.free_point
        if p:
            p_free = p if p < self.free_point else self.free_point
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
        """
        Check if the character has reached the maximum reset count based
        on the current level and stats.
        """
        print(">>>Func: check_max_reset")
        try:
            if self.lvl < 600:
                return False
            if self.added_point == self.MAX_POINTS * 4:
                print("Max reset!")
                self.max_reset = True
                return True
        except Exception as e:
            _raise(e)

    def add_all_point(self):
        """
        Add all available free points to the character's stats,
        prioritizing agility, energy, strength, and life in that order.
        """
        print(">>>Func: add_all_point")
        while not self.check_max_reset() and self.free_point != 0:
            self.cur_stat()
            if self.add_point(Point.AGILITY):
                time.sleep(4)
                self.cur_reset()
                continue
            if self.add_point(Point.ENERGY):
                time.sleep(4)
                self.cur_reset()
                continue
            if self.add_point(Point.LIFE):
                time.sleep(4)
                self.cur_reset()
                continue
            if self.add_point(Point.STRENGTH):
                time.sleep(4)
                self.cur_reset()
        return True
