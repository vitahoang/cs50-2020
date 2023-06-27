import time

from models.resources import Command
from utils import click, chat

npc_reset = {
    "name": "NPC Reset",
    "map": "arena",
    "map_lv2": "arena_npc",
    "command": Command().PK,
    "map_loc": {"x": 55, "y": 165},
    "click_loc": {"x": 540, "y": 420}
}

npc_master = {
    "name": "Master Reset",
    "map": "noria",
    "map_lv2": "NPCMR",
    "command": Command().RM,
    "map_loc": {"x": 196, "y": 113},
    "click_loc": {"x": 719, "y": 135}
}


class NPC:
    name: str
    map: str
    map_lv2: str
    command: str
    map_loc: dict
    click_loc: dict

    def __init__(self, npc):
        self.name = npc["name"]
        self.map = npc["map"]
        self.map_lv2 = npc["map_lv2"]
        self.command = npc["command"]
        self.map_loc = npc["map_loc"]
        self.click_loc = npc["click_loc"]

    def click_npc(self):
        chat(self.command)
        time.sleep(6)
        click(_loc=self.click_loc)
