import getpass
import pickle
import re

user_name = "/Users/" + getpass.getuser()
best_server: str
best_time: int


class Resource:
    def look_up_by_val(self, val: str = None):
        var = {}
        for i in dir(self):
            if re.search("__", i):
                break
            var[str(eval("self." + i))] = i
        try:
            if val:
                return var[val]
            return var
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
    VIP3 = {"x": 910, "y": 435}
    VIP4 = {"x": 896, "y": 462}
    VIP5 = {"x": 879, "y": 493}
    VIP6 = {"x": 910, "y": 530}
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


class TrainingServer(Resource):
    def __init__(self, _name=None, _time=None):
        self.name = _name
        self.train_time = _time
        self.prev_train_time = None

    def new_train(self, _time):
        self.prev_train_time = self.train_time
        self.train_time = _time

    def update_server_list(self):
        server_list = self.load_server_list()
        for server in server_list:
            if server.name == self.name:
                server_list.remove(server)
        server_list.append(self)
        with open('server.pkl', 'wb') as f:
            pickle.dump(server_list, f)
        f.close()

    @staticmethod
    def load_server_list():
        try:
            with open('server.pkl', 'rb') as f:
                server_list = pickle.load(f)
                print(type(server_list))
                f.close()
                return server_list
        except IOError:
            raise

    def pick_server(self):
        global best_server, best_time
        server_list = self.load_server_list()
        best_server = server_list[0].name
        best_time = server_list[0].train_time

        for server in server_list:
            if best_time > server.train_time:
                best_server = server.name
                best_time = server.train_time
            return best_server
