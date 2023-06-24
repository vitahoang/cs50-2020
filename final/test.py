from models.character import Character
from utils import find_item
from models.resources import Item

print(find_item(Item.VIP, region=(794, 1000, 1306, 1588)))
character = Character()
character.cur_loc()
character.cur_lvl()
character.cur_stat()