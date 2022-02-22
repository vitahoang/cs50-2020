import string


def main():
    """main()
    """
    text = ""
    while len(text) < 1:
        text = input("Text: ")
    index = coleman_liau_index(text_counter(text))
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def text_counter(text) -> dict:
    """
    count number of sentences, words, character in a text

    Args:
        text (str): text
    Returns:
        counter: {"sentences": int, "words": int, "characters": int}
    """
    counter = {"sentences": 0, "words": 1, "characters": 0}
    for i in text:
        if i in ("!", "?", "."):
            counter["sentences"] += 1
        if i == " ":
            counter["words"] += 1
        if i in string.ascii_letters:
            counter["characters"] += 1
    return counter


def coleman_liau_index(counter) -> int:
    """
    return Coleman Liau index

    Args:
        counter (dict): return from text_counter()
    Returns:
        index (int)
    """
    L = counter["characters"] / counter["words"] * 100
    S = counter["sentences"] / counter["words"] * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(index)


if __name__ == "__main__":
    main()
