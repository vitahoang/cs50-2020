import getpass
import re

user_name = "/Users/" + getpass.getuser()


class Resource:
    def look_up_by_val(self, val: str):
        var = {}
        for i in dir(self):
            if re.search("__", i):
                break
            var[str(eval("self." + i))] = i
        try:
            return var[val]
        except KeyError:
            return False


class FolderPath(Resource):
    ITEM = user_name + "/Code/cs50-2020/final/items/"
    IMAGE = user_name + "/Code/cs50-2020/final/images/"
    SAMPLE = user_name + "/Code/cs50-2020/final/samples/"
    MODEL = user_name + "/Code/cs50-2020/final/models/upscale/"


class Point(Resource):
    STRENGTH = "/f "
    AGILITY = "/a "
    LIFE = "/v "
    ENERGY = "/e "


class Command(Resource):
    ARENA11 = "/arena11"
    ARENA7 = "/arena7"
    RM = "/npcmr"
    PK = "/npcpk"
    NORIA = "/move Noria"
    LORENCIA = "/move Lorencia"


class Screen(Resource):
    OPEN = "open"
    START = "start"
    SERVER = "server"
    CHARACTER = "character"
    IN_GAME = "in_game"


class ItemLoc(Resource):
    START = {"x": 1175, "y": 769}
    VIP = {"x": 720, "y": 428}
    SPOT = {"x": 724, "y": 450}
    SPOT5 = {"x": 890, "y": 480}
    SPOT6 = {"x": 909, "y": 527}
    VIP4 = {"x": 896, "y": 462}
    VIP5 = {"x": 879, "y": 493}
    C_MAGIC = {"x": 1042, "y": 522}
    C_ENTER = {"x": 723, "y": 777}
    RS_RIGHT = {"x": 559, "y": 461}
    RS_LEFT = {"x": 885, "y": 465}
    RS_SEND = {"x": 724, "y": 600}
    MOVE_LEFT = {"x": 175, "y": 781}
    MOVE_RIGHT = {"x": 307, "y": 307}
    MOVE_UP = {"x": 256, "y": 683}
    MOVE_DOWN = {"x": 258, "y": 839}
    ATTACK_EVIL = {"x": 1244, "y": 809}
    ATTACK_TWISTING = {"x": 1119, "y": 846}
    STAT_MENU = {"x": 1287, "y": 118}
    ATTACK_HAND = {"x": 1113, "y": 766}
    CHAT = {"x": 1027, "y": 825}
    SETTING = {"x": 1066, "y": 38}
    CHANGE_SERVER = {"x": 724, "y": 385}
    INVENTORY = {"x": 1282, "y": 66}
    PARTY_CANCEL = {"x": 769, "y": 546}
    PARTY_OK = {"x": 671, "y": 544}
    DISCONNECTED = {"x": 721, "y": 543}


a = Command()
a.look_up_by_val("/arena11")
