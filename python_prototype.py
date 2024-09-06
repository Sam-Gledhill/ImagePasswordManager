# Prototype of the main c++ project in python - shows that it is possible to store small images inside of images

import cv2 as cv
import numpy as np
from numba import njit
import os
import sys


@njit
def encode_data(img, string):
    index = 0

    for i, n in enumerate(img):
        for j, m in enumerate(n):
            if index == len(string):
                return img
            r, g, b, a = img[i, j]
            a -= ord(string[index])
            img[i, j] = [r, g, b, a]
            index += 1

    raise Exception("Dest image too small!!")

# decode breaks with njit


def decode_data(img):

    data_string = ""

    for i, n in enumerate(img):
        for j, m in enumerate(n):
            r, g, b, a = img[i, j]
            data = 255-a

            if data == 0:
                return data_string

            data_string += chr(data)

    raise Exception("Could not find encoded data!")


def encode_image(dest_img_path, secret_image_path):
    image = cv.imread(dest_img_path)
    image = cv.cvtColor(image, cv.COLOR_RGB2RGBA)

    secret_string = str(cv.imread(secret_image_path).tolist())

    print("Encoding...")
    encoded_image = encode_data(image, secret_string)
    print("Encoded")

    cv.imwrite(dest_img_path, encoded_image)


def decode_image(encoded_image_path):

    read_img = cv.imread(encoded_image_path, cv.IMREAD_UNCHANGED)

    print("Decoding...")
    secret_image = np.array(eval(decode_data(read_img)), dtype=np.uint8)
    print("Decoded")

    # Sets the encoded image to rgb instead of rgba
    image = cv.imread(encoded_image_path)
    cv.imwrite(encoded_image_path, image)

    cv.imwrite(".decoded_" + encoded_image_path, secret_image)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        _, dest, secret = sys.argv
        encode_image(dest, secret)

    elif len(sys.argv) == 2:
        _, encoded = sys.argv
        decode_image(encoded)

    else:
        raise Exception("Invalid arguments")
