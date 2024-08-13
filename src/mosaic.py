"""Class for defining the global image that will be filled as Mosaic

Returns:
    _type_: image
"""

import PIL.Image
import numpy as np

class Mosaic:
    """class for the Mosaic image
    """

    def __init__(self, img_path):
        self.__img_path = img_path
        self.__img_pil = PIL.Image.open(img_path)
        self.__img_arr = np.asarray(self.__img_pil)

    def get_img_path(self) -> str:
        """getter for image path

        Returns:
            str: image path string
        """
        return self.__img_path

    def get_img_pil(self) -> PIL.Image.Image:
        """getter for PIL Image

        Returns:
            PIL.Image.Image: PIL Image
        """
        return self.__img_pil

    def get_img_arr(self) -> np.ndarray:
        """getter for img array

        Returns:
            np.ndarray: image array
        """
        return self.__img_arr
