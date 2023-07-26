import logging
from threading import Thread

from control import *
from models.character import Character
from models.resources import Screen, ItemLoc, TrainingServer
from utils import click

# global var
screen = None
max_reset = False
server_list = TrainingServer().load_server_list()
server_name = ["VIP3", "VIP4", "VIP5", "VIP6"]
server = TrainingServer().pick_server()
print(f"Server: {server}")
train_time: int

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


def check_screen_thread(timeout=12):
    global screen
    q = Queue(maxsize=1)
    e = Event()
    threads = []
    for screen_name in list(Screen().look_up_by_val().keys()):
        print(f"Start {screen_name} thread")
        threads.append(Thread(target=check_screen, args=(screen_name, q, e)))
    for thread in threads:
        thread.start()
    start_time = time.time()
    while not q.full() and time.time() - start_time < timeout:
        time.sleep(1)
        print("Screen checking...")
    if q.full():
        screen = q.get()
        print(f"Screen is on {screen}")
        return screen
    else:
        return False


def run():
    global screen, max_reset, server, server_name, train_time

    # check which screen is showing
    check_party()
    check_disconnected()
    # if failed, try to open the app
    if not check_screen_thread():
        if open_app() is False:
            logging.error("Open App Failed")
            return False
        time.sleep(5)
        screen = check_screen(screen_name=Screen.START)

    # else, login
    match screen:
        case Screen.START:
            click(_loc=ItemLoc.START)
            time.sleep(4)
            join_server(server)
        case Screen.SERVER:
            join_server(server)
        case Screen.CHARACTER:
            select_character()
    screen = Screen.IN_GAME

    character = Character()
    character.cur_reset()
    while not character.max_reset:
        character.cur_reset()

        # train after reset
        if character.reset < 1:
            train_after_reset(character)

        start_time = time.time()
        # normal train
        if train(character):
            # update train time
            if character.reset > 1:
                train_time = int(round((time.time() - start_time)))
                print(f"Train time: {train_time}")
                TrainingServer(_name=server, _time=train_time).update_server_list()
                server = TrainingServer().pick_server()

            # add point and reset
            character.add_all_point()
            if character.max_reset and solve_captcha(master=True):
                character.max_reset = False
            else:
                solve_captcha(server=server)
        else:
            return False
    if character.max_reset and solve_captcha(master=True):
        character.max_reset = False


if __name__ == "__main__":
    main()
