from menu import MenuMap, MenuChat
from npc import NPC

# screenWidth, screenHeight = pyautogui.size()
# print(screenWidth, screenHeight)
# currentMouseX, currentMouseY = pyautogui.position()
# print(currentMouseY, currentMouseY)
menu_map = MenuMap()
menu_chat = MenuChat()


def main():
    # Login
    # if open_app() is False:
    #     sys.exit("Open App Failed")
    # if click_item(Item.START) is False:
    #     sys.exit("Start Failed")
    # if click_item(Item.VIP) is False:
    #     sys.exit("Join Sever Failed")
    # if click_item(Item.VIP5, 1) is False:
    #     sys.exit("Join Sever Failed")
    # if click_item(Item.C_MAGIC) is False:
    #     sys.exit("Select Character Failed")
    # if click_item(Item.C_ENTER, 1) is False:
    #     sys.exit("Select Character Failed")

    # Reset
    NPC(npc_name="reset").click_npc()
    # Master Reset
    NPC(npc_name="master_reset").click_npc()


if __name__ == "__main__":
    main()
