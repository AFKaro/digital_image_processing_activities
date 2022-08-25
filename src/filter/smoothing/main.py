import numpy as np
import cv2 as cv

DELAY_BLUR = 100

window_name = 'my_filter'

def get_filter(src: any, size: int, filter: int):
    if filter == 1:
        return cv.blur(src, (size, size))
    if filter == 2: 
        return cv.medianBlur(src, size)
    elif filter == 3:
        return cv.GaussianBlur(src, (size, size), 0)

def run_filter(image: any, num_applications: int, size: int, filter: int):
    src = image
    for i in range(num_applications):
        src = get_filter(src, size, filter)
        compare = np.concatenate((image, src), axis=1)
        cv.imshow(window_name, compare)
        cv.waitKey(DELAY_BLUR)

def print_image() -> any:
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    origin = cv.imread(f"./src/archives/peppers_gray_ruido.bmp")
    cv.imshow(window_name, origin)
    return origin

if __name__=="__main__":

    origin = print_image()
    ascii_code = 48
    option = 1

    while (True):

        print("[1] - Blur \n"
              "[2] - Median Blur \n"
              "[3] - Gaussian Blur \n"
              "[4] - Reset \n"
              "[0] - Exit")
        
        print("Select option: ")
        option = cv.waitKey() - ascii_code

        if option == 0:
            break

        if option == 4:
            origin = print_image()
        else:
            print("Number applications: ")
            num_applications = cv.waitKey()  - ascii_code

            print("Size: ")
            mask_size = cv.waitKey()  - ascii_code
            run_filter(image=origin, 
                    num_applications=num_applications, 
                    size=mask_size,
                    filter=option)