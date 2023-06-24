import time

from models.character import Character
from control import open_app, join_server, check_screen, solve_captcha, \
    train_after_reset, train
from utils import pop_err, click
from models.npc import NPC
from models.resources import ItemLoc, Map, Screen


def main():
    if open_app() is False:
        pop_err("Open App Failed")
    time.sleep(5)
    character = Character()
    for _ in range(3):
        if character.cur_loc():
            break
        click(item_loc=ItemLoc.START)
        if check_screen() != Screen.SERVER:
            pop_err("Start Failed")
            break
        time.sleep(5)
        join_server()

    character.cur_lvl()
    character.cur_stat()
    if character.reset == 0:
        train_after_reset(character)
    if train(character):
        NPC(npc_name="master_reset").click_npc()
        solve_captcha()


if __name__ == "__main__":
    main()
