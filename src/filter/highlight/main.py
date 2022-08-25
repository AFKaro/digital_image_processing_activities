import numpy as np
import cv2 as cv

DELAY_BLUR = 100

window_name = 'highlight_filter'

def get_filter(image: any, filter: int):

    scale = 1
    delta = 0
    ddepth = cv.CV_16S

    # Sobel
    if filter == 1:
        grad_x = cv.Sobel(image, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
        grad_y = cv.Sobel(image, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)

    # Prewitt
    elif filter == 2: 
        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])

        grad_x = cv.filter2D(image, -1, kernel_x)
        grad_y = cv.filter2D(image, -1, kernel_y)
    
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)

    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    return grad

def run_filter(image: any, filter: int):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    img_gaussian = cv.GaussianBlur(gray, (3,3), 0)

    new_image = get_filter(img_gaussian, filter)

    compare = np.concatenate((img_gaussian, new_image), axis=1)
    cv.imshow(window_name, compare)
    cv.waitKey(DELAY_BLUR)

def print_image(img: any) -> any:
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    origin = cv.imread(img)
    cv.imshow(window_name, origin)
    return origin

def select_image(img_num: int) -> any:
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

        print("[1] - Sobel \n"
              "[2] - Prewitt \n"
              "[3] - Reset \n"
              "[4] - Select image \n"
              "[0] - Exit")
        
        print("Select option: ")
        option = cv.waitKey() - ascii_code

        if option == 0:
            break

        elif option == 3:
            origin = print_image(origin_img)

        elif option == 4:
            print("Image Number: ")
            origin_img = select_image(cv.waitKey() - ascii_code)
            origin = print_image(origin_img)

        else:

            run_filter(image=origin, 
                       filter=option)