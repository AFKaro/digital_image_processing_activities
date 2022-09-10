import sys

sys.path.append("./src")

from utils.image_functions import select_image
import cv2 as cv
import numpy as np

DELAY_BLUR = 100

window_name = 'equalize'

def probability_gray_level(image_gray: list) -> list:

    image_array = np.array(image_gray)
    levels = np.unique(image_array)

    prob_levels = []
    for level in levels:
        prob_levels.append([level, np.count_nonzero(image_array == level) / (len(image_gray)*len(image_gray[0]))])
    
    return prob_levels

def cumulative_distribution(prob_levels: list) -> list:

    for i in range(1, len(prob_levels)):
        prob_levels[i][1] = prob_levels[i][1] + prob_levels[i-1][1]
    
    return prob_levels

def cumulative_values_by_max_gray(cummulative: list) -> list:

    max_gray = cummulative[-1][0]

    for val in cummulative:
        val[1] = int(val[1] * max_gray)
    
    return cummulative

def map_new_levels(image: list, new_levels: list) -> list:

    for lines in image:
        for value in lines:
            value = search_level(new_levels, value)
    
    return image

def search_level(levels: list, value: int) -> int:
    
    for level in levels:
        if level[0] == value:
            return level[1]
    return 0

def hist_equalize(image: list):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    prob_levels = probability_gray_level(gray)
    cummulative = cumulative_distribution(prob_levels)
    new_levels = cumulative_values_by_max_gray(cummulative)

    new_image = map_new_levels(gray, new_levels)


    compare = np.concatenate((gray, new_image), axis=1)
    cv.imshow(window_name, compare)
    cv.waitKey(DELAY_BLUR)

def print_image(img: any) -> any:
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    origin = cv.imread(img)
    cv.imshow(window_name, origin)
    return origin

if __name__=="__main__":
    origin_img = f"./src/archives/lena.png"
    origin = print_image(origin_img)
    ascii_code = 48
    option = 1

    while (True):

        print("[1] - Equalize Histogram \n"
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
            hist_equalize(origin)