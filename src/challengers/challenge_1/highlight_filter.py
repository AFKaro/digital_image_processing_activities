from dataclasses import dataclass
import numpy as np
import cv2 as cv


@dataclass
class HighlightFilter:
    
    def filter(self, image: list, filter_num: int) -> list:
        scale = 1
        delta = 0
        ddepth = cv.CV_16S

        # Sobel
        if filter_num == 1:
            grad_x = cv.Sobel(image, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
            grad_y = cv.Sobel(image, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)

        # Prewitt
        elif filter_num == 2: 
            kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
            kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])

            grad_x = cv.filter2D(image, -1, kernel_x)
            grad_y = cv.filter2D(image, -1, kernel_y)
        
        abs_grad_x = cv.convertScaleAbs(grad_x)
        abs_grad_y = cv.convertScaleAbs(grad_y)

        grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad
        