import sys

sys.path.append("./src")

from utils.image_functions import select_image
import cv2 as cv
import numpy as np

DELAY_BLUR = 100

window_name = 'segmentation'


def get_limiar(image_array: list) -> float:
    t_ref = 0

    # Select an estimated value for T (midpoint between the minimum and maximum values of an image)
    levels = np.unique(image_array)
    t_value = (levels[0] + levels[-1]) / 2
    t_value_ant = t_ref

    iterations = 0

    while ((t_value - t_value_ant) != t_ref):
        # Segment the image using T
        left = []
        rigth = []

        for line in range(0, len(image_array)):
            for col in range(0, len(image_array[line])):
                if (image_array[line][col] < t_value):
                    left.append(image_array[line][col])
                else:
                    rigth.append(image_array[line][col])

        # Calculate the average of the pixel intensities in each region
        mean_left = np.mean(left) if left else 0
        mean_rigth = np.mean(rigth) if rigth else 0

        # Calculate the new value of T
        t_value_ant = t_value
        t_value = (mean_left + mean_rigth) / 2

        iterations +=1
        print(f"Iteration: {iterations}, T Value: {t_value}, Mean Left: {mean_left}, Mean Rigth: {mean_rigth}")
    
    return t_value


def segmentation(image: list):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    limiar = get_limiar(gray)

    _, dst = cv.threshold(gray, limiar, 255, 0)

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