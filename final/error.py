import sys

from pymsgbox import alert


def raise_err(text="", title="Error", button="OK"):
    alert(text=text, title=title, button=button)
    sys.exit(text)

