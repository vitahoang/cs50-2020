# Import required packages
import cv2
import pytesseract

from resources import FolderPath

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = \
    "/opt/homebrew/Cellar/tesseract/5.3.1_1/bin/tesseract"


def extract_text_from(img):
    # Preprocessing the image starts

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = img.copy()

    # A text file is created and flushed
    _file = open("recognized.txt", "w+")
    _file.write("")
    _file.close()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Open the file in append mode
        # _file = open("recognized.txt", "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        # Appending the text into file
        # _file.write(text)
        # _file.write("\n")

        # Close the file
        # _file.close()
        return text


def cur_map_loc(image):
    info = extract_text_from(image).replace("\n", "").split(" ")
    _map = {
        "map_name": info[0],
        "x": info[2],
        "y": info[3]
    }
    print(_map)
    return _map


def cur_char_lvl(image):
    info = extract_text_from(image).replace("\n", "").split(" ")
    _char = {
        "character_name": info[0],
        "lvl": info[2]
    }
    print(_char)
    return _char


cur_map_loc(cv2.imread(FolderPath.SAMPLE + "map-info.png"))

cur_char_lvl(cv2.imread(FolderPath.SAMPLE + "char-lvl.png"))
