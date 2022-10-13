import numpy as np
import cv2 as cv
import sys


sys.path.append("./src")

from challengers.challenge_2.highlight_filter import HighlightFilter
from challengers.challenge_2.smoothing_filter import SmoothingFilter
from challengers.challenge_2.histogram import Histogram
from challengers.challenge_2.controller import Controller
from segmentation.region.application.connectivity_strategy_interface import ConnectivityStrategyInterface
from segmentation.region.application.eigth_connectivity_strategy import EigthConnectivityStrategy
from segmentation.region.application.four_connectivity_strategy import FourConnectivityStrategy
from segmentation.region.application.m_connectivity_strategy import MConnectivityStrategy


DELAY_BLUR = 100

window_name = 'segmentation'

seed_x = 0
seed_y = 0
origin = None
region = None

def click_event(event, y, x, flags, params):
    if event == cv.EVENT_RBUTTONDOWN:
        print(f"Seed: [{x},{y}]")

        global seed_x
        global seed_y
        seed_x = x
        seed_y = y

def grad_img(image: list) -> list:
    highlight = HighlightFilter()
    return highlight.filter(image, 1)

def segmentation(image: list, connective: ConnectivityStrategyInterface):
    controller = Controller(image)
    controller.execute(seed_x=seed_x, seed_y=seed_y, connective=connective)
    global origin
    origin = controller.image
    
    global region
    region = controller.region

def histogram(image: list):
    levels = np.unique(image)
    print(f"Min Level: {levels[0]}, Max Level: {levels[-1]}")
    
    hist = Histogram(image)
    hist.plot()

def print_image(img: list) -> list:
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    global origin
    origin = cv.imread(img)
    cv.imshow(window_name, origin)
    return origin

def print_region(src: str) -> list:
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    img = cv.imread(src)
    global region
    
    for line in range(len(img)):
        for col in range(len(img[line])):
            if region.exist_pixel(line, col):
                img[line][col] = 0
            else:
                img[line][col] = 255

    cv.imshow("segmentation", img)
    cv.waitKey(10)


if __name__=="__main__":
    origin_img = f"./src/challengers/challenge_1/figure.png"
    origin = print_image(origin_img)
    origin = cv.cvtColor(origin, cv.COLOR_BGR2GRAY)
    ascii_code = 48
    option = 1

    while (True):

        print("[1] - Segmentation \n"
              "[2] - Highlight \n"
              "[3] - Histogram \n"
              "[4] - Print Region \n"
              "[5] - Reset \n"
              "[0] - Exit")
        
        print("Select option: ")
        cv.setMouseCallback(window_name, click_event)
        option = cv.waitKey() - ascii_code
        #origin = grad_img(image=origin)

        if option == 0:
            break

        elif option == 1:
            while option != 0:
                print("[1] - 4-Connectivity \n"
                "[2] - 8-Connectivity \n"
                "[3] - M-Connectivity \n"
                "[0] - Return")
            
                print("Select option: ")
                option = cv.waitKey() - ascii_code

                if option == 1:
                    segmentation(origin, FourConnectivityStrategy)
                elif option == 2:
                    segmentation(origin, EigthConnectivityStrategy)
                elif option == 3:
                    segmentation(origin, MConnectivityStrategy)
                else: 
                    print("Invalid option!")
                    
        elif option == 2:
             smothing_alg = SmoothingFilter()
             origin = smothing_alg.smothing(origin)
             cv.imshow(window_name, origin)
             
        elif option == 3:
            histogram(origin)
        
        elif option == 4:
            origin = print_region(origin_img)
            
        elif option == 5:
            origin = print_image(origin_img)
        
        else:
            print("Invalid option!")