"""
This module defines the NPC class and two NPC objects, npc_reset and npc_master. 
The NPC class stores information about an NPC, including its name, location, and command to execute. 
The npc_reset object represents an NPC in the arena map, while npc_master represents an NPC in the noria map. 
Usage:
   npc_reset.click_npc() # clicks the npc_reset object
   npc_master.click_npc() # clicks the npc_master object
Attributes:
   name (str): the name of the NPC
   map (str): the name of the map where the NPC is located
   map_lv2 (str): the name of the sub-map where the NPC is located
   command (str): the command to execute when interacting with the NPC
   map_loc (dict): the x and y coordinates of the NPC's location on the map
   click_loc (dict): the x and y coordinates of the NPC's location when clicked
Methods:
   click_npc(): executes the NPC's command and clicks on the NPC
"""
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
    """
    A class to represent an NPC in the game.
     Attributes:
        name (str): the name of the NPC
        map (str): the name of the map where the NPC is located
        map_lv2 (str): the name of the sub-map where the NPC is located
        command (str): the command to execute when interacting with the NPC
        map_loc (dict): the x and y coordinates of the NPC's location on the map
        click_loc (dict): the x and y coordinates of the NPC's location when clicked
    """
    name: str
    map: str
    map_lv2: str
    command: str
    map_loc: dict
    click_loc: dict

    def __init__(self, npc):
        """
        Initializes an NPC object with the given attributes.
         Args:
            npc (dict): a dictionary containing the attributes of the NPC
        """
        self.name = npc["name"]
        self.map = npc["map"]
        self.map_lv2 = npc["map_lv2"]
        self.command = npc["command"]
        self.map_loc = npc["map_loc"]
        self.click_loc = npc["click_loc"]

    def click_npc(self):
        """
        Executes the NPC's command and clicks on the NPC.
        """
        chat(self.command)
        time.sleep(6)
        click(_loc=self.click_loc)
