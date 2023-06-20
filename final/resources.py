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


class Point:
    strength = "/f "
    agility = "/a "
    life = "/v "
    energy = "/e "
