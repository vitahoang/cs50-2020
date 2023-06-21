import getpass

user_name = "/Users/" + getpass.getuser()


class FolderPath:
    ITEM = user_name + "/Code/cs50-2020/final/items/"
    IMAGE = user_name + "/Code/cs50-2020/final/images/"
    SAMPLE = user_name + "/Code/cs50-2020/final/samples/"
    MODEL = user_name + "/Code/cs50-2020/final/models/"


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
    MV_LEFT = {"x": 175, "y": 781}


class Point:
    strength = "/f "
    agility = "/a "
    life = "/v "
    energy = "/e "


class Map:
    arena11 = "/arena11"
    rm = "/npcmr"
    pk = "/npcpk"
    noria = "/move Noria"
    lorencia = "/move Lorencia"
