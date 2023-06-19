# Note

Use the below instruction if you have troubles using opencv and pyautogui packages

### Install opencv

As an alternate to adding the cv2 path into the interpreter, symlink the cv2/cv2.abi3.so file (cv2.pyd in WIndows?) into
the site-packages dir. For example, in site-packages:
```ln -s cv2/cv2.abi3.so```

### Install pyautogui

https://github.com/python-poetry/poetry/issues/4322#issuecomment-1590796737

### TypeError: '<' not supported between instances of 'str' and 'int'

So you need to click into the reported error file. Replace this code:

```if tuple(PIL__version__) < (6, 2, 1):```
with this code:

```if tuple(map(int, PIL__version__.split("."))) < (6, 2, 1):```