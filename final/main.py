from control import *
from models.character import Character
from models.npc import NPC, npc_reset
from models.resources import Screen, ItemLoc
from utils import pop_err, click

screen: int
max_reset = False


def main():
    global screen, max_reset
    # Open App
    # if open_app() is False:
    #     pop_err("Open App Failed")
    #     return False
    # time.sleep(5)

    screen = check_screen()
    match screen:
        case None:
            pop_err("Open App Failed")
            return False
        case Screen.START:
            click(_loc=ItemLoc.START)
            time.sleep(4)
            join_server()
        case Screen.SERVER:
            join_server()
        case Screen.CHARACTER:
            select_character()
    screen = Screen.IN_GAME

    character = Character()
    while not max_reset:
        character.check_max_reset()
        if character.reset < 1:
            train_after_reset(character)
        if train(character):
            character.add_all_point()
            max_reset = character.check_max_reset()
            if max_reset:
                NPC(npc=npc_master).click_npc()
                if solve_captcha(master=True):
                    max_reset = False
                    screen = Screen.SERVER
                    continue
            NPC(npc=npc_reset).click_npc()
            if solve_captcha():
                screen = Screen.SERVER


if __name__ == "__main__":
    main()
