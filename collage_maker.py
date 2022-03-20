# -*- coding: utf-8 -*-
"""
Collage maker - tool to create picture collages
Author: Delimitry
"""

import argparse
import os
import random
from PIL import Image

from random import seed, randint


def make_collage(images, filename, width, height, init_height):
    """
    Make a collage image with a width equal to `width` from `images` and save to `filename`.
    """
    if not images:
        print("No images for collage found!")
        return False

    margin_size = 0
    # run until a suitable arrangement of images is found
    seed(69)

    images_list = images[:]
    y = 0
    collage_image = Image.new("RGB", (width, height), (35, 35, 35))

    while y <= height:
        images_row = []
        x = 0
        while x <= width:
            img_path = images_list[randint(0, len(images_list) - 1)]
            img = Image.open(img_path)
            img.thumbnail((width, init_height))
            x += img.size[0] + margin_size
            images_row.append(img_path)

        coef = x / width
        pos_x = 0
        for img_path in images_row:
            img = Image.open(img_path)
            k = (init_height / coef) / img.size[1]
            img = img.resize(
                (int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS
            )
            collage_image.paste(img, (pos_x, y))
            pos_x += img.size[0]

        y += int(init_height / coef) + margin_size

    collage_image.save(filename)
    return True


def main():
    # prepare argument parser
    parse = argparse.ArgumentParser(description="Photo collage maker")
    parse.add_argument(
        "-f",
        "--folder",
        dest="folder",
        help="folder with images (*.jpg, *.jpeg, *.png)",
        default=".",
    )
    parse.add_argument(
        "-o",
        "--output",
        dest="output",
        help="output collage image filename",
        default="collage.png",
    )
    parse.add_argument(
        "-w", "--width", dest="width", type=int, help="resulting collage image width"
    )
    parse.add_argument(
        "-hi",
        "--height",
        dest="height",
        type=int,
        help="resulting collage image height",
    )
    parse.add_argument(
        "-i",
        "--init_height",
        dest="init_height",
        type=int,
        help="initial height for resize the images",
    )
    parse.add_argument(
        "-s",
        "--shuffle",
        action="store_true",
        dest="shuffle",
        help="enable images shuffle",
    )

    args = parse.parse_args()
    if not args.width or not args.init_height:
        parse.print_help()
        exit(1)

    # get images
    files = [os.path.join(args.folder, fn) for fn in os.listdir(args.folder)]
    images = [
        fn
        for fn in files
        if os.path.splitext(fn)[1].lower() in (".jpg", ".jpeg", ".png")
    ]
    if not images:
        print(
            "No images for making collage! Please select other directory with images!"
        )
        exit(1)

    # shuffle images if needed
    if args.shuffle:
        random.shuffle(images)

    print("Making collage...")
    res = make_collage(images, args.output, args.width, args.height, args.init_height)
    if not res:
        print("Failed to create collage!")
        exit(1)
    print("Collage is ready!")


if __name__ == "__main__":
    main()
