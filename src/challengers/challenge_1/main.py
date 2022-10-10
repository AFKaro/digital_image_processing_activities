import numpy as np
import cv2 as cv
import sys

sys.path.append("./src")

from challengers.challenge_1.highlight_filter import HighlightFilter
from challengers.challenge_1.histogram import Histogram
from challengers.challenge_1.controller import Controller


DELAY_BLUR = 100

window_name = 'challenge'

def grad_img(image: list) -> list:
    highlight = HighlightFilter()
    return highlight.filter(image, 1)

def segmentation(image: list):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    controller = Controller(gray)
    # Init T selecionado conforme histograma
    new_img = controller.execute(init_t=120)

    compare = np.concatenate((gray, new_img), axis=1)
    cv.imshow(window_name, compare)
    cv.waitKey(DELAY_BLUR)

def histogram(image: list):
    levels = np.unique(image)
    print(f"Min Level: {levels[0]}, Max Level: {levels[-1]}")
    
    hist = Histogram(image)
    hist.plot()

def print_image(img: any) -> any:
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    origin = cv.imread(img)
    cv.imshow(window_name, origin)
    return origin


if __name__=="__main__":
    origin_img = f"./src/challengers/challenge_1/figure.png"
    origin = print_image(origin_img)
    ascii_code = 48
    option = 1

    while (True):

        print("[1] - Segmentation \n"
              "[2] - Histogram \n"
              "[3] - Reset \n"
              "[0] - Exit")
        
        print("Select option: ")
        option = cv.waitKey() - ascii_code
        origin = grad_img(image=origin)

        if option == 0:
            break

        elif option == 1:
            segmentation(origin)
            
        elif option == 2:
            histogram(origin)
            
        elif option == 3:
            origin = print_image(origin_img)
        
        else:
            print("Invalid option!")