import sys

from control import open_app, click_item
from error import raise_err
from menu import MenuMap, MenuChat
from npc import NPC
from resources import Item

# screenWidth, screenHeight = pyautogui.size()
# print(screenWidth, screenHeight)
# currentMouseX, currentMouseY = pyautogui.position()
# print(currentMouseY, currentMouseY)
menu_map = MenuMap()
menu_chat = MenuChat()


def main():
    # Login
    if open_app() is False:
        raise_err("Open App Failed")
    if click_item(Item.START) is False:
        raise_err("Start Failed")
    if click_item(Item.VIP) is False:
        raise_err("Join Sever Failed")
    if click_item(Item.VIP5, 1) is False:
        raise_err("Join Sever Failed")
    if click_item(Item.C_MAGIC) is False:
        raise_err("Select Character Failed")
    if click_item(Item.C_ENTER, 1) is False:
        raise_err("Select Character Failed")

    # Reset
    NPC(npc_name="reset").click_npc()
    # Master Reset
    NPC(npc_name="master_reset").click_npc()


if __name__ == "__main__":
    main()
