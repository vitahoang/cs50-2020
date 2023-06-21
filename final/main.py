from character import Character
from control import open_app, click_item
from error import raise_err
from menu import MenuMap, MenuChat
from npc import NPC
from reset import solve_captcha
from resources import Item, ItemLoc, Map

menu_map = MenuMap()
menu_chat = MenuChat()
_char = Character()


def main():
    # Login
    # if open_app() is False:
    #     raise_err("Open App Failed")
    # if click_item(loc=ItemLoc.START) is False:
    #     raise_err("Start Failed")
    # if click_item(Item.VIP) is False:
    #     raise_err("Join Sever Failed")
    # if click_item(Item.VIP5, 1) is False:
    #     raise_err("Join Sever Failed")
    # if click_item(Item.C_MAGIC) is False:
    #     raise_err("Select Character Failed")
    # if click_item(Item.C_ENTER, 1) is False:
    #     raise_err("Select Character Failed")

    # Reset
    # NPC(npc_name="reset").click_npc()
    # solve_captcha()
    # Master Reset
    # NPC(npc_name="master_reset").click_npc()
    _char.train()


if __name__ == "__main__":
    main()
