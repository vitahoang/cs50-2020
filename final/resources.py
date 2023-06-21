import getpass

user_name = getpass.getuser()


class FolderPath:
    ITEM = "/Users/" + user_name + "/Code/cs50-2020/final/item/"
    IMAGE = "/Users/" + user_name + "/Code/cs50-2020/final/image/"


class Item:
    START = "start.png"
    VIP = "vip.png"
    SPOT = "spots.png"
    SPOT5 = "spots5.png"
    VIP5 = "vip5.png"
    C_MAGIC = "character-magic.png"
    C_ENTER = "character-enter.png"


class ItemLoc:
    START = {"x": 1175, "y": 769}
    VIP = {}
    SPOT = {}
    SPOT5 = {}
    VIP5 = {}
    C_MAGIC = {}
    C_ENTER = {}
    RS_RIGHT = {"x": 559, "y": 461}
    RS_LEFT = {"x": 885, "y": 465}
    RS_SEND = {"x": 724, "y": 590}


class Point:
    strength = "/f "
    agility = "/a "
    life = "/v "
    energy = "/e "