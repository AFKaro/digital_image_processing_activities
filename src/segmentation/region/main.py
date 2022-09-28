import sys

sys.path.append("./src")

from segmentation.region.application.connectivity_strategy_interface import ConnectivityStrategyInterface
from segmentation.region.application.segmentation_by_region_context import SegmentationByRegionContext
from segmentation.region.application.eigth_connectivity_strategy import EigthConnectivityStrategy
from segmentation.region.application.four_connectivity_strategy import FourConnectivityStrategy
from segmentation.region.models.region import Region
from utils.image_functions import select_image
import cv2 as cv


DELAY_BLUR = 100
seed_x = 0
seed_y = 0

window_name = 'segmentation'

def click_event(event, y, x, flags, params):
    if event == cv.EVENT_RBUTTONDOWN:
        print(f"Seed: [{x},{y}]")

        global seed_x
        global seed_y
        seed_x = x
        seed_y = y


def segmentation(image: list, connective: ConnectivityStrategyInterface):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    segmentation_alg = SegmentationByRegionContext()
    segmentation_alg.set_strategy(connective(gray))
    segmentation_alg.segment(seed_x, seed_y)
    region = segmentation_alg.get_region()

    new_image = mark_region(gray.copy(), region)
    cv.imshow(window_name, new_image)
    cv.waitKey(DELAY_BLUR)


def mark_region(image: list, region: Region):
    for pixel in region.pixels:
        image[pixel.x, pixel.y] = 0
    return image


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

        elif option == 1:
            while option != 0:
                print("[1] - 4-Connectivity \n"
                "[2] - 8-Connectivity \n"
                "[3] - M-Connectivity \n"
                "[0] - Return")
            
                print("Select option: ")
                option = cv.waitKey() - ascii_code

                if option == 1:
                    segmentation(origin, EigthConnectivityStrategy)
                elif option == 2:
                    segmentation(origin, FourConnectivityStrategy)
                elif option == 3:
                    print("In development...")
                else: 
                    print("Invalid option!")
        
        else:
            print("Invalid option!")