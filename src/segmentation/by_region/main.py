import sys

sys.path.append("./src")

from segmentation.by_region.segmentation_by_region import SegmentationRegionAlgorithm
from utils.image_functions import select_image
import cv2 as cv

DELAY_BLUR = 100
seed_x = 0
seed_y = 0

window_name = 'segmentation'

def click_event(event, x, y, flags, params):
    if event == cv.EVENT_RBUTTONDOWN:
        print(f"Seed: [{x},{y}]")

        global seed_x
        global seed_y
        seed_x = x
        seed_y = y

def segmentation(image: list):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    segmentation_alg = SegmentationRegionAlgorithm(gray)
    segmentation_alg.segmentation(seed_x, seed_y)
    regions = segmentation_alg.regions
    # compare = np.concatenate((gray, dst), axis=1)
    # cv.imshow(window_name, compare)
    # cv.waitKey(DELAY_BLUR)


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
        cv.setMouseCallback(window_name, click_event)
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