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
        self.__mean = self.set_img_mean()

    def set_img_mean(self) -> int:
        """set image mean

        Returns:
            int: return int of mean value of pixels
        """
        image_stat = PIL.ImageStat.Stat(self.get_pil_img())
        mean = int(image_stat.mean[0])
        return mean

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
        # TODO : mieux gérer l'exception
        if res.status_code == 200:
            image_url = res.json()["data"]["images"]["original"]["url"]
        else:
            print("ERROR WHILE FETCHING DATA ---------------")
            print('Status code : ', res.status_code)
            print("res.content : ", res.content)
            return ""
        return image_url

    def load_pil_img(self) -> PIL.Image:
        """loads the image from the url as a PIL.Image

        Returns:
            PIL.Image: PIL.Image
        """
        try:
            res = requests.get(url=self.__url, timeout=5)
            image_data = BytesIO(res.content)
            image = PIL.Image.open(image_data).convert("L")
            return image
        except requests.exceptions.MissingSchema as e :
            print("ERROR : ", e)

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
