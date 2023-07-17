# MuAwayAuto

#### Video Demo:  <URL HERE>

#### Description:

My final project is a bot designed to automate gameplay in the MuOnline game. The game follows simple rules:

- Players must train their characters to reach the maximum level.
- With each level gained, players receive stat points that enhance their character's abilities
- Upon reaching the maximum level, players can choose to perform a reset, resetting their level to 1 while retaining
  their accumulated stats. This allows them to continue training and gaining more stats.
- After several resets, the character will eventually reach its maximum stat potential. At this point, players can
  perform a master reset and receive rewards. The objective is to create a program that can automate this process.

My project consists of three main components: the controller functions responsible for character control, supporting
classes, and the most challenging part, the computer vision functions used to solve captchas during resets and master
resets.

The control file includes the following functions:

- Open app: Uses AppScript to open the game app in full-screen mode.
- Log in, join server, select character: Assists in logging into the game and choosing a character.
- Move character, train the character, reset the character: Enables control over the character's movements and training
  progress.

The models folder contains the following files:

- Character: Contains the character classes that track the character's level, stats, location, number of resets, and
  stat allocation.
- Image: Includes models used for image processing.
- Item: Helps locate and retrieve the screen coordinates of in-game items.
- Menu: Aids in navigating the game's menu system.
- NPC: Assists in navigating to in-game non-player characters (NPCs).
- Resources: Stores constant values relevant to the game.

While designing this app, I implemented several improvements:

- Instead of using a database to store constant values of the game, I utilized Python's data class, reducing the
  implementation effort required.
- To improve runtime, I optimized the search method from the pyautogui package by specifying a search area instead of
  searching the entire screen.
- Solving the captcha puzzle required a substantial amount of time and effort. The puzzle object possesses a symmetry
  point and an orientation, and users must rotate it to find the correct vertical orientation. To address this
  challenge, I developed a pipeline that combines various computer vision techniques:

    1. I used the dnn_superres model from OpenCV to upscale the image.
    2. The rembg package was employed to remove the background and isolate the object.
    3. To calculate the object's symmetry line, I utilized the following
       repository: https://github.com/dramenti/symmetry.
- These improvements were implemented to enhance the efficiency and functionality of the app.

# Installation

Use the below instruction if you have troubles install dependency packages

#### Install opencv

As an alternate to adding the cv2 path into the interpreter, symlink the cv2/cv2.abi3.so file (cv2.pyd in Windows?) into
the site-packages dir. For example, in site-packages, use this script if you create your env with poetry:

```
(cd $(poetry env list --full-path | \
grep -o '\/Users.*\s(Activated)' | cut -d " " -f 1)\
"/lib/python"\
$(poetry env list --full-path | \
 grep -Po '\-py.*\s\(Activated\)' | grep -Po '\d\.\d{1,2}')\
"/site-packages/"; ln -s cv2/cv2.abi3.so)
```

#### Install tesseract

-

readmore: https://www.oreilly.com/library/view/building-computer-vision/9781838644673/95de5b35-436b-4668-8ca2-44970a6e2924.xhtml

- Then you need to change location of the tesseract model in ```text.py```. You should find your model located in
  ```/opt/homebrew/Cellar/tesseract/...```

#### Install pyautogui

https://github.com/python-poetry/poetry/issues/4322#issuecomment-1590796737

#### TypeError: '<' not supported between instances of 'str' and 'int'

So you need to click into the reported error file. Replace this code:

```
if tuple(PIL__version__) < (6, 2, 1):
```

with this code:

```
if tuple(map(int, PIL__version__.split("."))) < (6, 2, 1):
```

#### No module named '_tkinter'

If you use pyenv to manage your Python versions (which you should), you'll run into this issue. I was able to fix it by
following these two steps.

1. Install necessary system packages:

- Install necessary system packages:
  ```brew install tcl-tk openssl readline sqlite3 xz zlib```
- Uninstall the current version
  ```export PY_VER=$(python --version | cut -d " " -f 2) pyenv uninstall $(echo $PY_VER)```
- Link the correct versions of Tcl/Tk
    ```
    env LDFLAGS="-L$(brew --prefix openssl@1.1)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix sqlite3)/lib -L$(brew --prefix xz)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix tcl-tk)/lib" \
    CPPFLAGS="-I$(brew --prefix openssl@1.1)/include -I$(brew --prefix readline)/include -I$(brew --prefix sqlite3)/include -I$(brew --prefix xz)/include -I$(brew --prefix zlib)/include -I$(brew --prefix tcl-tk)/include" \
    PKG_CONFIG_PATH="$(brew --prefix openssl@1.1)/lib/pkgconfig:$(brew --prefix readline)/lib/pkgconfig:$(brew --prefix sqlite3)/lib/pkgconfig:$(brew --prefix xz)/lib/pkgconfig:$(brew --prefix zlib)/lib/pkgconfig:$(brew --prefix tcl-tk)/lib/pkgconfig" \
    PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
    pyenv install $(echo $PY_VER)
    ```

- readmore: https://github.com/python-poetry/poetry/issues/4322#issuecomment-1574852226

