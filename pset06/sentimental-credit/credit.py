import sys


def main():
    """main()"""

    while True:
        str_card = input("Number: ")
        try:
            card = [int(i) for i in str_card]
        except ValueError:
            continue
        if card:
            break

    if len(card) < 13 or len(card) > 16 or check_luh_sum(card) is False:
        print("INVALID")
        sys.exit(0)

    if len(card) == 15 and card[0] == 3 and card[1] in (4, 7):
        print("AMEX")
    elif len(card) in (13, 16) and card[0] == 4:
        print("VISA")
    elif len(card) == 16 and card[0] == 5 and card[1] in range(1, 6):
        print("MASTERCARD")
    else:
        print("INVALID")


def check_luh_sum(card) -> bool:
    """
    An algorithm invented by Hans Peter Luhn of IBM to checksum the 
    credit card number
    """
    lsum = 0
    for i in range(len(card) - 2, -1, -2):
        if card[i] * 2 > 9:
            lsum = lsum + 1 + card[i] * 2 - 10
            continue
        lsum += card[i] * 2

    for i in range(len(card) -1 , -1, -2):
        lsum += card[i]

    if lsum % 10 == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
