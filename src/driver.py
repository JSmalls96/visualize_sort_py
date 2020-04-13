import numpy as np
from imageio import imwrite, get_reader
from skimage import color
import argparse
import os
from PIL import Image, ImageTk
from sorts import *

max_moves = 0
moves = []


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sorter', help="which sorting algorithm to use (bubble)", required=True)
    return parser.parse_args()


def generate_image():
    # hsv works in range 0 - 1
    img = np .zeros((300, 300, 3), dtype='float32')

    # in order to get a perfect rainbow, we need to have a
    # 1. consistent saturation, and hue
    # 2. shuffle it to be ready to sort
    for i in range(img.shape[1]):
        img[:, i, :] = i / img.shape[1], 1.0, 1.0

    # rgb_img is the original image
    # rgb_img = color.convert_colorspace(img, 'hsv', 'rgb')
    # imwrite('../images/initial_hsv_01.png', rgb_img)

    for i in range(img.shape[0]):
        np.random.shuffle(img[i, :, :])

    # imwrite('../images/initial_hsv_01_shuffled.png', color.convert_colorspace(img, 'hsv', 'rgb'))

    return img


def get_sort_selection(image, args):
    global max_moves, moves
    for i in range(image.shape[0]):
        new_moves = []
        if args.sorter == 'bubble':
            _, new_moves = bubble_sort(list(image[i, :, 0]))

        if len(new_moves) > max_moves:
            max_moves = len(new_moves)
        moves.append(new_moves)


def swap_pixels(img, row, places):
    tmp = img[row, places[0], :].copy()
    img[row, places[0], :] = img[row, places[1], :]
    img[row, places[1], :] = tmp


def to_movie(image, args):
    current_move = 0

    # 24 fps, and we want a 5 second gif 24 * 5 = 120 total frames (* 24 5)
    movie_image_step = max_moves // 120
    movie_image_frame = 0

    os.makedirs(args.sorter, exist_ok=True)

    while current_move < max_moves:
        for i in range(image.shape[0]):
            if current_move < len(moves[i]) - 1:
                swap_pixels(image, i, moves[i][current_move])

        if current_move % movie_image_step == 0:
            imwrite('%s/%05d.png' % (args.sorter, movie_image_frame), color.convert_colorspace(image, 'HSV', 'RGB'))
            movie_image_frame += 1
        current_move += 1


def main():
    args = get_input()
    img = generate_image()
    get_sort_selection(img, args)
    to_movie(img, args)
    os.chdir(args.sorter)
    os.system('ffmpeg -i %05d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p ready4gif.mp4')
    os.system('ffmpeg -i ready4gif.mp4 -vf fps=10,scale=320:-1:flags=lanczos,palettegen palette.png')
    os.system('ffmpeg -i ready4gif.mp4 -i palette.png -filter_complex "fps=10,scale=500:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif')
    os.system('output.gif')


if __name__ == '__main__':
    main()
