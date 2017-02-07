import argparse

import os
from termcolor import cprint
from scipy import misc
import matplotlib.pyplot as plt
from edges import __version__, detect


def main():
    parser = argparse.ArgumentParser(description='Image edges for cs 558')
    parser.add_argument('-v', '--version', action='version', version=__version__)

    parser.add_argument('-i', '--inputs', nargs='*', help="The input images to process.", required=True)
    parser.add_argument('-od', '--out-dir', help="The input images to process.", default='./out')

    parser.add_argument('-gs', '--gaussian-sigma', help="Filter operation to perform.", default=1)

    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    for image_path in args.inputs:
        try:
            processed = detect(image_path, args.gaussian_sigma)
        except Exception as ex:
            raise ex
            cprint('Error processing ' + image_path + ": " + str(ex), 'red')
            continue

        image_root, image_filename = os.path.split(image_path)
        out_path = os.path.join(args.out_dir, image_filename)

        plt.imshow(processed)
        misc.imsave(out_path, processed)


if __name__ == '__main__':
    main()
