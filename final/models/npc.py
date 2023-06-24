import time

from utils import click
from models.menu import MenuMap


class NPC:
    map: str
    map_lv2: str
    map_loc: dict
    click_loc: dict
    reset = {
        "map": "arena",
        "map_lv2": "arena_npc",
        "map_loc": {"x": 55, "y": 165},
        "click_loc": {"x": 540, "y": 420}
    }

    master_reset = {
        "map": "noria",
        "map_lv2": "NPCMR",
        "map_loc": {"x": 196, "y": 113},
        "click_loc": {"x": 719, "y": 135}
    }

    def __init__(self, npc_name: str):
        npc = None
        if npc_name == "reset":
            npc = self.reset
        if npc_name == "master_reset":
            npc = self.master_reset
        self.map = npc["map"]
        self.map_lv2 = npc["map_lv2"]
        self.map_loc = npc["map_loc"]
        self.click_loc = npc["click_loc"]

    def click_npc(self):
        menu_map = MenuMap()
        eval("menu_map.map_" + self.map + "(self.map_lv2)")
        time.sleep(3)
        click(self.click_loc["x"], self.click_loc["y"])
