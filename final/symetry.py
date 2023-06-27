"""
Performs symmetry detection on an image using SIFT for keypoint detection and a voting mechanism in the Hough space for line of symmetry detection.
First, it computes the keypoints and descriptors of the image and its mirror image. Then, it matches these keypoints and for each match, it computes the midpoint, the angle with the x-axis, and the 'r' value in polar coordinates. It then votes for this line in the Hough space using a weight computed from the Reisfeld function and the 'S' function.
Finally, it returns the coordinates of the most voted for line in the Hough space.
Note: To visualize the voting process in the Hough space, set plot=True. This will display a 3D histogram where the most voted for line of symmetry is indicated by bright orange/red. Manually get the coordinates, and re-run but this time uncomment draw/imshow.
Parameters:
    image (ndarray): The input image.
    plot (bool): If True, plots a 3D histogram of the voting process in the Hough space.
Returns:
    tuple: The coordinates of the most voted for line in the Hough space.
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray

sift = cv2.SIFT_create()


def very_close(a, b, tol=4.0):
    """Checks if the points a, b are within
    tol distance of each other."""
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) < tol


def S(si, sj, sigma=1):
    """Computes the 'S' function mentioned in
    the research paper."""
    q = (-abs(si - sj)) / (sigma * (si + sj))
    return np.exp(q ** 2)


def reisfeld(phi, phj, theta):
    return 1 - np.cos(phi + phj - 2 * theta)


def midpoint(i, j):
    return (i[0] + j[0]) / 2, (i[1] + j[1]) / 2


def angle_with_x_axis(i, j):
    x, y = i[0] - j[0], i[1] - j[1]
    if x == 0:
        return np.pi / 2
    angle = np.arctan(y / x)
    if angle < 0:
        angle += np.pi
    return angle


def superm2(image, plot=False):
    mimage = np.fliplr(image)
    kp1, des1 = sift.detectAndCompute(image, None)
    kp2, des2 = sift.detectAndCompute(mimage, None)
    for p, mp in zip(kp1, kp2):
        p.angle = np.deg2rad(p.angle)
        mp.angle = np.deg2rad(mp.angle)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    houghr = np.zeros(len(matches))
    houghth = np.zeros(len(matches))
    weights = np.zeros(len(matches))
    i = 0
    good = []
    for match, match2 in matches:
        point = kp1[match.queryIdx]
        mirpoint = kp2[match.trainIdx]
        mirpoint2 = kp2[match2.trainIdx]
        mirpoint2.angle = np.pi - mirpoint2.angle
        mirpoint.angle = np.pi - mirpoint.angle
        if mirpoint.angle < 0.0:
            mirpoint.angle += 2 * np.pi
        if mirpoint2.angle < 0.0:
            mirpoint2.angle += 2 * np.pi
        mirpoint.pt = (mimage.shape[1] - mirpoint.pt[0], mirpoint.pt[1])
        if very_close(point.pt, mirpoint.pt):
            mirpoint = mirpoint2
            good.append(match2)
        else:
            good.append(match)
        theta = angle_with_x_axis(point.pt, mirpoint.pt)
        xc, yc = midpoint(point.pt, mirpoint.pt)
        r = xc * np.cos(theta) + yc * np.sin(theta)
        Mij = reisfeld(point.angle, mirpoint.angle, theta) * S(
            point.size, mirpoint.size
        )
        houghr[i] = r
        houghth[i] = theta
        weights[i] = Mij
        i += 1
    # matches = sorted(matches, key = lambda x:x.distance)
    good = sorted(good, key=lambda x: x.distance)

    # img3 = cv2.drawMatches(image, kp1, mimage, kp2, good[:15], None, flags=2)

    # print(*(m.distance for m in matches[:10]))
    # cv2.imshow('a',img3); cv2.waitKey(0);
    def hex():
        if plot:
            plt.hexbin(houghr, houghth, bins=200, gridsize=50)
            plt.show()
        pcol = plt.hexbin(houghr, houghth, bins=200, gridsize=50)
        # get the most density bin from the hexbin plot
        max_ = pcol.get_array().max()
        max_pos = pcol.get_array().argmax()

        # return the coordination of the bin which act as (r,theta)
        pos_x, pos_y = pcol.get_offsets()[max_pos]
        plt.text(pos_x, pos_y, max_, color='w')
        return round(float(pos_x), 2), round(float(pos_y), 2)

    return hex()

    # draw(2.8, 2.4)
    # cv2.imshow('a', image); cv2.waitKey(0);


def draw(image: ndarray, r, theta):
    result = image.copy()
    if np.pi / 4 < theta < 3 * (np.pi / 4):
        for x in range(len(result.T)):
            y = int((r - x * np.cos(theta)) / np.sin(theta))
            if 0 <= y < len(result.T[x]):
                result[y][x] = 255
    else:
        for y in range(len(result)):
            x = int((r - y * np.sin(theta)) / np.cos(theta))
            if 0 <= x < len(result[y]):
                result[y][x] = 255
    return result.copy()
