"""
    Method to create a BDD of images to fulfil mosaic
"""

import json
from tqdm import tqdm
from constants import NUMBER_IMG
from image_gif import ImageGif

if __name__ == '__main__':

    # load json existing
    with open('./image_bdd.json', "r", encoding='UTF-8') as outfile:
        # palette dict
        dict_palette = json.load(outfile)
        for i in range(255):
            dict_palette[i] = []

        # load image from url (100)
        for i in tqdm(range(NUMBER_IMG)):
            try:
                img = ImageGif()
                dict_palette[img.get_mean()].append(img.get_url())
            except KeyError as e:
                print("KeyError : ", e)

        # save dict of images
    with open("./image_bdd.json", "w", encoding="UTF-8") as outfile:
        json.dump(dict_palette, outfile)
