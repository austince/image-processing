import argparse

import os
import sys
from termcolor import cprint
from scipy import misc
import matplotlib.pyplot as plt
from edges import __version__
from edges.operations.detection import detect
from edges.operations.gaussian import filter_image as gaussian_filter
from edges.operations.suppression import threshold_image


def main():
    parser = argparse.ArgumentParser(description='Image edges for cs 558')
    parser.add_argument('-v', '--version', action='version', version=__version__)

    parser.add_argument('-i', '--input', help="The input image to process.", required=True, type=str)
    parser.add_argument('-o', '--output', help="Where to put the output.", default=None, type=str)

    parser.add_argument('-gs', '--gaussian-sigma', help="Sigma for gaussian filter", default=1, type=int)
    parser.add_argument('-t', '--threshold', help="Threshold for non max suppression", default=100, type=int)

    parser.add_argument('-og', '--only-gaussian', help="Only do gaussian filter.",
                        dest='only_gaussian', action='store_true')
    parser.add_argument('-ogm', '--only-grad-mag', help="Only do gradient magnitude.",
                        dest='only_grad_mag', action='store_true')

    args = parser.parse_args()

    try:
        cprint('Processing file: ' + str(args.input), 'green')
        image = misc.imread(args.input)

        if args.only_gaussian:
            cprint('Only gaussian filtering!', 'green')
            processed = gaussian_filter(image, args.gaussian_sigma)
        elif args.only_grad_mag:
            cprint('Only gradient magnitude!', 'green')
            processed = gaussian_filter(image, args.gaussian_sigma)
            processed = threshold_image(processed, args.threshold)
        else:
            # cprint('Detecting edges!', 'green')
            processed = detect(image, args.gaussian_sigma, args.threshold)

    except FileNotFoundError:
        cprint("Can't load image file: " + str(args.input), 'red')
        sys.exit(1)
    except Exception as ex:
        # raise ex  # For Development
        cprint('Error processing ' + args.input + ": " + str(ex), 'red')
        sys.exit(1)

    cprint('Done!', 'green')

    if args.output:
        image_dir, image_filename = os.path.split(args.output)

        if image_dir and not os.path.exists(image_dir):
            os.makedirs(image_dir)

        out_path = args.output
    else:
        input_dir, input_filename = os.path.split(args.input)
        out_path = "./edges." + input_filename

    # plt.imshow(processed)
    misc.imsave(out_path, processed)


if __name__ == '__main__':
    main()
