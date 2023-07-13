import logging

from control import *
from models.character import Character
from models.npc import NPC, npc_reset
from models.resources import Screen, ItemLoc
from utils import click

# global var
screen: int
max_reset = False

# Configure logging
logging.basicConfig(filename='app.log', filemode='w',
                    datefmt='%d-%b-%y %H:%M:%S',
                    format='### %(asctime)s:%(name)s:%(levelname)s:%('
                           'message)s')
logging.info('This will get logged to a file')


def main():
    while True:
        try:
            logging.info("Start MuAway Auto App")
            run()
        except Exception as e:
            logging.critical(e, exc_info=True)
            time.sleep(5)


def run():
    global screen, max_reset

    # check which screen is showing
    check_party()
    screen = check_screen()
    # if failed, try to open the app
    if not screen or check_disconnected():
        if open_app() is False:
            logging.error("Open App Failed")
            return False
        time.sleep(5)
        screen = check_screen(screen=Screen.START)

    # else, login
    match screen:
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
