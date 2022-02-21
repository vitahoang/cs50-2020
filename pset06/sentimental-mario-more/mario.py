# TODO
import sys

if len(sys.argv) != 2:
    sys.exit("Usage: python mario.py PYRAMIDHEIGHT")

height = int(sys.argv[1])
for i in range(height+1):
    space = " " * (height - i)
    lv = "#" * i
    print(f"{space}{lv}  {lv}")
