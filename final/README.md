# Note

Use the below instruction if you have troubles install dependency packages

### Install opencv

As an alternate to adding the cv2 path into the interpreter, symlink the cv2/cv2.abi3.so file (cv2.pyd in Windows?) into
the site-packages dir. For example, in site-packages, use this script if you create your env with poetry:

```
(cd $(poetry env list --full-path | \
grep -o '\/Users.*\s(Activated)' | cut -d " " -f 1)\
"/lib/python"\
$(poetry env list --full-path | \
grep -o '\/Users.*\s(Activated)' | cut -d " " -f 1 | grep -o '\d\.\d')\
"/site-packages/"; ln -s cv2/cv2.abi3.so)
```

### Install tesseract

https://www.oreilly.com/library/view/building-computer-vision/9781838644673/95de5b35-436b-4668-8ca2-44970a6e2924.xhtml
Then you need to change location of the tesseract model in ```text.py```. You should find your model located in
```/opt/homebrew/Cellar/tesseract/...```

### Install pyautogui

https://github.com/python-poetry/poetry/issues/4322#issuecomment-1590796737

### TypeError: '<' not supported between instances of 'str' and 'int'

So you need to click into the reported error file. Replace this code:

```
if tuple(PIL__version__) < (6, 2, 1):
```

with this code:

```
if tuple(map(int, PIL__version__.split("."))) < (6, 2, 1):
```

### No module named '_tkinter'

https://github.com/python-poetry/poetry/issues/4322#issuecomment-1574852226

