import numpy as np
import cv2 as cv
import numpy as np

DELAY_BLUR = 100

window_name = 'histogram'

def hist(image: any):
    histSize = 256
    histRange = (0, 256)
    accumulate = False
    bgr_planes = cv.split(image)

    b_hist = cv.calcHist(bgr_planes, [0], None, [histSize], histRange, accumulate=accumulate)
    g_hist = cv.calcHist(bgr_planes, [1], None, [histSize], histRange, accumulate=accumulate)
    r_hist = cv.calcHist(bgr_planes, [2], None, [histSize], histRange, accumulate=accumulate)

    hist_w = 512
    hist_h = 400
    bin_w = int(round( hist_w/histSize ))

    histImage = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

    cv.normalize(b_hist, b_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
    cv.normalize(g_hist, g_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
    cv.normalize(r_hist, r_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)

    for i in range(1, histSize):
        cv.line(histImage, ( bin_w*(i-1), hist_h - int(b_hist[i-1]) ), ( bin_w*(i), hist_h - int(b_hist[i]) ), ( 255, 0, 0), thickness=2)
        cv.line(histImage, ( bin_w*(i-1), hist_h - int(g_hist[i-1]) ), ( bin_w*(i), hist_h - int(g_hist[i]) ), ( 0, 255, 0), thickness=2)
        cv.line(histImage, ( bin_w*(i-1), hist_h - int(r_hist[i-1]) ), ( bin_w*(i), hist_h - int(r_hist[i]) ), ( 0, 0, 255), thickness=2)

    compare = np.concatenate((image, histImage), axis=0)
    cv.imshow(window_name, compare)
    cv.waitKey(DELAY_BLUR)

def print_image(img: any) -> any:
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    origin = cv.imread(img)
    cv.imshow(window_name, origin)
    return origin

def select_image(img_num: int) -> any:
    new_img = f"./src/archives/lena.png"

    if img_num == 1:
        new_img = f"./src/archives/lena.png"
    elif img_num == 2:
        new_img = f"./src/archives/airplane.png"
    elif img_num == 3:
        new_img = f"./src/archives/baboon.png"
    elif img_num == 4:
        new_img = f"./src/archives/fruits.png"
    elif img_num == 5:
        new_img = f"./src/archives/peppers.png"
    
    return new_img

if __name__=="__main__":
    origin_img = f"./src/archives/lena.png"
    origin = print_image(origin_img)
    ascii_code = 48
    option = 1

    while (True):

        print("[1] - Histogram \n"
              "[2] - Reset \n"
              "[3] - Select image \n"
              "[0] - Exit")
        
        print("Select option: ")
        option = cv.waitKey() - ascii_code

        if option == 0:
            break

        elif option == 2:
            origin = print_image(origin_img)

        elif option == 3:
            print("Image Number: ")
            origin_img = select_image(cv.waitKey() - ascii_code)
            origin = print_image(origin_img)

        else:
            hist(image=origin)