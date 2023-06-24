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
    COLLAPSE = "collapse.png"


class ItemLoc:
    START = {"x": 1175, "y": 769}
    VIP = {"x": 720, "y": 428}
    SPOT = {"x": 724, "y": 450}
    SPOT5 = {"x": 890, "y": 480}
    VIP4 = {"x": 896, "y": 462}
    VIP5 = {"x": 879, "y": 493}
    C_MAGIC = {"x": 1044, "y": 565}
    C_ENTER = {"x": 723, "y": 777}
    RS_RIGHT = {"x": 559, "y": 461}
    RS_LEFT = {"x": 885, "y": 465}
    RS_SEND = {"x": 724, "y": 590}
    MOVE_LEFT = {"x": 175, "y": 781}
    MOVE_RIGHT = {"x": 307, "y": 307}
    ATTACK_EVIL = {"x": 1244, "y": 809}
    STAT_MENU = {"x": 1287, "y": 118}
    ATTACK_HAND ={"x": 1115, "y": 766}


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


class Screen:
    START = "start"
    SERVER = "server"
    CHARACTER = "character"
    IN_GAME = "in_game"
