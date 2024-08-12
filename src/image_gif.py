"""_summary_

Class to instanciate images from Giphy and get mean and load easily using the API

Returns:
    _type_: gets a fully Image object with url to get from giphy and info
"""

import os
from io import BytesIO
import PIL.Image
import PIL.ImageStat
import requests
from dotenv import load_dotenv


class ImageGif:
    """Class for images from giphy API"""

    def __init__(self):
        self.__url = self.get_random_url()
        self.__pil_img = self.load_pil_img()
        self.__mean = int((PIL.ImageStat.Stat(self.__pil_img)).mean()[0])

    def get_random_url(self) -> str:
        """get a random gif from giphy APIs

        Returns:
            str: random image url from giphy
        """
        load_dotenv()
        res = requests.get(
            url=os.environ.get("GIPHY_URL"),
            params={"api_key": os.environ.get("GIPHY_API_KEY")},
            timeout=5,
        )
        image_url = res.json()["data"]["images"]["original"]["url"]
        return image_url

    def load_pil_img(self) -> PIL.Image:
        """loads the image from the url as a PIL.Image

        Returns:
            PIL.Image: PIL.Image
        """
        res = requests.get(url=self.__url, timeout=5)
        image_data = BytesIO(res.content)
        image = PIL.Image.open(image_data).convert("L")
        return image

    def get_pil_img(self) -> PIL.Image:
        """getter of PIL image

        Returns:
            PIL.Image: PIL.Image
        """
        return self.__pil_img

    def get_mean(self) -> int:
        """mean of pixels getter

        Returns:
            int: mean value of all pixels on image
        """
        return self.__mean

    def get_url(self) -> str:
        """absolute URL of image

        Returns:
            str: url path of image
        """
        return self.__url
