while True:
    try:
        h = int(input("Height: "))
    except ValueError:
        continue
    if h > 0 and h < 9:
        break

for i in range(1, h+1):
    space = " " * (h - i)
    lv = "#" * i
    print(f"{space}{lv}  {lv}")