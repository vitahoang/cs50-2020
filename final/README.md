# MuAwayAuto

#### Video Demo:  <URL HERE>

#### Description:

MuAwayAuto is an advanced tool that automates character training in the game MuAway. It utilizes the pyautogui package for character control, an OCR package for data updates from the game, and an ML image pipeline to solve captchas for level resets and claim rewards. This powerful tool streamlines tasks and optimizes progress for an easy gaming experience in MuAway.

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

- readmore: https://www.oreilly.com/library/view/building-computer-vision/9781838644673/95de5b35-436b-4668-8ca2-44970a6e2924.xhtml
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

