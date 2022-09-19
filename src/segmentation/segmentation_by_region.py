import sys

sys.path.append("./src")

from utils.image_functions import select_image
import cv2 as cv
import numpy as np

DELAY_BLUR = 100

window_name = 'segmentation'


def dif_gray_levels(pixel: int, seed: int, min_gray: int) -> bool:
    return np.abs(pixel - seed) <= 10/100 * (255 - min_gray)

def verify_four_neighbor(img: list, seed: tuple) -> bool:
    x = seed[0]
    y = seed[1]
    value_seed = img[x][y]

    if (dif_gray_levels(img[x + 1][y], value_seed)):
        pass

    if (dif_gray_levels(img[x - 1][y], value_seed)):
        pass
    
    if (dif_gray_levels(img[x][y + 1], value_seed)):
        pass

    if (dif_gray_levels(img[x][y - 1], value_seed)):
        pass

def region(img: list, seed: tuple):
    pass


def get_new_img(image_array: list, limiar: float) -> list:
    new_img = image_array.copy()

    for line in range(0, len(new_img)):
        for col in range(0, len(new_img[line])):
            if (new_img[line][col] < limiar):
                new_img[line][col] = 0
            else:
                new_img[line][col] = 255
    return new_img


def segmentation(image: list):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    limiar = get_limiar(gray)

    dst = get_new_img(gray, limiar)

    compare = np.concatenate((gray, dst), axis=1)
    cv.imshow(window_name, compare)
    cv.waitKey(DELAY_BLUR)


def print_image(img: any) -> any:
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    origin = cv.imread(img)
    cv.imshow(window_name, origin)
    return origin


if __name__=="__main__":
    origin_img = f"./src/archives/digital.jpg"
    origin = print_image(origin_img)
    ascii_code = 48
    option = 1

    while (True):

        print("[1] - Segmentation \n"
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
            segmentation(origin)