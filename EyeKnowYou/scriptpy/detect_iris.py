from matplotlib import pyplot as plt
import cv2
import numpy as np
import argparse

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
cropped = False

def bottom_hat_median_blurr(image):
    """
    Bottom hat filtering and smoothing with median filter
    :param image: image
    :return: filtered image
    """
    cimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    blackhat = cv2.morphologyEx(cimg, cv2.MORPH_BLACKHAT, kernel)
    bottom_hat_filtered = cv2.add(blackhat, cimg)
    return cv2.medianBlur(bottom_hat_filtered, 17)


def adjust_gamma(image, gamma=1.0):
    """
    Building a lookup table mapping the pixel values [0, 255] to
    their adjusted gamma values. Increasing contrast
    :param image: image
    :param gamma: adjusting coefficient
    :return: adjusted image
    """
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)



def detect_inner_circle(img, canny_param=20, hough_param=20):
    """
    Detecting inner iris circle after filtering
    :param img: image
    :param canny_param: higher threshold for canny edge detector
    :param hough_param: threshold parameter for Hough circle transform
    :return:
    """
    filtered = bottom_hat_median_blurr(img)
    adjusted = adjust_gamma(filtered, 10)
    circles = cv2.HoughCircles(adjusted, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=canny_param,
                               param2=hough_param,
                               minRadius=0)
    inner_circle = [0, 0, 0]
    if circles is not None:
        inner_circle = np.uint16(np.around(circles[0][0])).tolist()
    return inner_circle


def detect_pupil(image):
    '''
    :param img_list: list containing file path to the images
    :return: displays the hough circle and returns the center of the circle
    '''
    img = image
    circle = detect_inner_circle(img)
    # cv2.circle(img, (circle[0], circle[1]), circle[2], (255, 0, 0), 2)
    # cv2.circle(img, (circle[0], circle[1] - int(circle[2] / 2)), 2, (0, 255, 0), 3)
    return circle[0] + int(circle[2] / 1.5) , circle[1] - int(circle[2] / 1.5) 


 
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, cropped
 
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        # print("click")
        refPt = [(x, y)]
        cropping = True
 
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        print("Center clicked")
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        # refPt.append((x, y))
        cropping = False
        cropped = True
 
        # # draw a rectangle around the region of interest
        # cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        # cv2.imshow("image", image)

def click_iris(cap):
    global cropped
    cropped = False
    ret, image = cap.read()
    print("Please click the center of area you want\n")
    cv2.namedWindow("Click the center of area you want")
    cv2.setMouseCallback("Click the center of area you want", click_and_crop)
    while(True):
        clone = image.copy()
        cv2.imshow("Click the center of area you want", image)
        key = cv2.waitKey(1) & 0xFF
        if(key == ord('q') or cropped):
            break
    if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[0][0], refPt[0][1] + 1 :refPt[0][0] + 1]
        cv2.imshow("ROI", roi)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

    return refPt[0][1], refPt[0][0]
# close all open windows


def get_cordinates(cap, mode="manual"):
    if(mode == "manual"):
        x, y = click_iris(cap)
        return x, y

    else:

        while(mode == "auto"):
            res = input("\n\nTurn your face towards the monitor. look at the middle of the monitor, keep your eyes open wide. This is will only take 5-10 seconds. Try to keep a low blinking frequency and type c and pres enter to continue. ")
            if(res == 'c'):
                break
        cx = []
        cy = []
        count = 0
        while(count <= 50):
            status = "Calibrating Frame" + "|" + "-" * count + "|"
            print(status, end="\r")
            ret, image = cap.read()
            x,y = detect_pupil(image)
            # print([x,y])
            cv2.circle(image, (x, y), 30, (0, 0, 255), 2)

            cv2.imshow('frame',image)
            cv2.waitKey(2)
            
            if(x != 0 or y != 0):
                cx.append(x)
                cy.append(y)
                count = count + 1

        vx = np.var(np.asarray(cx))
        vy = np.var(np.asarray(cy))
        ax = np.average(np.asarray(cx))
        ay = np.average(np.asarray(cy))
        sx = np.sum(np.asarray(cx))
        sy = np.sum(np.asarray(cy))
        outliers = 0
        for x,y in zip(cx,cy):
            if (np.abs(ax - x) > 20 or np.abs(ay - y) > 20):
                outliers = outliers + 1
                sx = sx - x
                sy = sy - y 
                # print("outliers = " + str(outliers))
        cordinates = [np.round(sx/(50-outliers)).astype(int), np.round(sy/(50-outliers)).astype(int)]
        # while True:
        #     ret, image = cap.read()
        #     cv2.circle(image, (cordinates[0], cordinates[1]), 30, (0, 255, 0), 2)
        #     cv2.imshow('frame',image)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        # print(cordinates)
        print("Calibration Successful !!!\n")
        cv2.destroyAllWindows()
        return np.round(sx/(50-outliers)).astype(int), np.round(sy/(50-outliers)).astype(int)    


# cap = cv2.VideoCapture(0)
# cx, cy = get_cordinates(cap)
# print(cx, cy)
# while True:
#     ret, image = cap.read()
#     cv2.circle(image, (np.round(np.average(np.asarray(cx))).astype(int), np.round(np.average(np.asarray(cy))).astype(int)), 30, (0, 255, 0), 2)
#     cv2.imshow('frame',image)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break