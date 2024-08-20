"""Class for defining the global image that will be filled as Mosaic

Returns:
    _type_: image
"""

import json
from io import BytesIO
from tqdm import tqdm
import PIL.Image
from PIL.image import BILINEAR
import numpy as np
import requests
from constants import TAILLE_DALLE, ALPHA

class Mosaic:
    """class for the Mosaic image
    """

    def __init__(self, img_path):
        """_summary_

        Args:
            img_path (String): path to the desired image for the mosaic
        """
        self.__img_path = img_path
        self.__img_pil = PIL.Image.open(img_path)
        self.__img_arr = np.asarray(self.__img_pil)
        self.__img_mosaic_arr = self.get_image_mosaic()
        self.__img_mosaic = PIL.Image.fromarray(self.__img_mosaic_arr)

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

    def get_image_mosaic(self) -> np.ndarray:
        """return the calculated mosaic image

        Returns:
            np.ndarray: array representing image mosaic
        """
        width, height = self.__img_pil.size
        new_w = width // ALPHA
        new_h = height // ALPHA
        output_arr = np.zeros((TAILLE_DALLE * new_w, TAILLE_DALLE * new_h))
        self.__img_pil = self.__img_pil.convert("L")
        self.__img_arr = np.asarray(
            self.__img_pil.resize([new_w, new_h], resample=BILINEAR)
        )
        with open("./image_bdd.json", 'r') as input:
            dict_url = json.load(input)
            for i in tqdm(range(new_w), desc="Processing rows"):
                for j in tqdm(range(new_w), desc="Processing columns", leave=False):
                    value = self.__img_arr[i, j]
                    if len(dict_url[str(self.__img_arr[i, j])]) > 0:
                        # il existe une image
                        # remplacer la nouvelle image par celle-ci
                        # prendre une image au pif
                        index = np.random.randint(len(dict_url[str(value)]))

                        # remplacer les pixels
                        image = self.load_img_from_url(
                            dict_url[str(value)][index]
                        ).resize((TAILLE_DALLE,  TAILLE_DALLE))

                        output_arr[
                            i*TAILLE_DALLE:(i+1)*TAILLE_DALLE,
                            j*TAILLE_DALLE:(j+1)*TAILLE_DALLE
                        ] = image
                    else:
                        output_arr[
                            i*TAILLE_DALLE:(i+1)*TAILLE_DALLE,
                            j*TAILLE_DALLE:(j+1)*TAILLE_DALLE
                        ] = 0
            return output_arr

    def load_img_from_url(self, url) -> PIL.Image.Image:
        """method to get a image from giphy API

        Args:
            url (String): URL to the given GIF image from Giphy

        Returns:
            PIL.Image.Image: PIL Object represnting the desired image
        """
        res = requests.get(url=url, timeout=5)
        image_data = BytesIO(res.content)
        image = PIL.Image.open(image_data).convert("L")
        return image

    def save_img_mosaic(self) -> None:
        """Method to save the mosaic generated
        """
        self.__img_mosaic.save('./images/output.gif')

if __name__ == '__main__':
    image = Mosaic("./images/moicassou.jpg")
    image.save_img_mosaic()
