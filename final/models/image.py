import cv2
import numpy as np

from models.resources import FolderPath


def upscale(image):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    path = FolderPath.MODEL + "FSRCNN-small_x3.pb"
    sr.readModel(path)
    sr.setModel("fsrcnn", 3)
    img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    result = sr.upsample(img)
    return result


def bg_remove_hsv(image):
    """Remove background using HSV mask"""
    # threshold on white
    # Define lower and upper limits
    lower = np.array([0, 0, 0])
    upper = np.array([0, 0, 130])

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    return output


def estimate_hsv(image):
    """Estimate HSV threshold of object to create extracted mask"""

    def nothing(x):
        pass

    # Create a window
    cv2.namedWindow('image')

    # create trackbars for color change
    cv2.createTrackbar('HMin', 'image', 0, 179,
                       nothing)  # Hue is from 0-179 for Opencv
    cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)

    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    output = image
    wait_time = 33

    while (1):

        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin', 'image')
        sMin = cv2.getTrackbarPos('SMin', 'image')
        vMin = cv2.getTrackbarPos('VMin', 'image')

        hMax = cv2.getTrackbarPos('HMax', 'image')
        sMax = cv2.getTrackbarPos('SMax', 'image')
        vMax = cv2.getTrackbarPos('VMax', 'image')

        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # Print if there is a change in HSV value
        if ((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (
                phMax != hMax) | (psMax != sMax) | (pvMax != vMax)):
            print(
                "(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
                    hMin, sMin, vMin, hMax, sMax, vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        # Display output image
        cv2.imshow('image', output)

        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def bg_remove_threshold(image):
    """Remove background using simple threshold mask"""
    # First Convert to Grayscale
    myimage_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, baseline = cv2.threshold(myimage_grey, 127, 255, cv2.THRESH_TRUNC)
    _, background = cv2.threshold(baseline, 126, 255, cv2.THRESH_BINARY)
    _, foreground = cv2.threshold(baseline, 126, 255, cv2.THRESH_BINARY_INV)

    # Update foreground with bitwise_and to extract real foreground
    foreground = cv2.bitwise_and(image, image, mask=foreground)

    return foreground
