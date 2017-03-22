import argparse
import os
import sys

from scipy import misc
from termcolor import cprint

from detection import __version__
from detection.operations import gaussian, canny, ransac, hessian, hough
from detection.operations.suppression import threshold_image


def main():
    parser = argparse.ArgumentParser(description='Image detection for cs 558')
    parser.add_argument('-v', '--version', action='version', version=__version__)

    parser.add_argument('-i', '--input', help="The input image to process.", required=True, type=str)
    parser.add_argument('-o', '--output', help="Where to put the output.", type=str)

    parser.add_argument('-gs', '--gaussian-sigma', help="Sigma for gaussian filter.", default=1, type=int)
    parser.add_argument('-t', '--threshold', help="Threshold for various suppression.", type=int)

    parser.add_argument('-op', '--operation', help="The operation to return.", required=True, type=str,
                        choices=[
                            'gaussian', 'g',
                            'gradient-magnitude', 'grad-mag', 'gm'
                            'edges', 'canny',
                            'ransac', 'rn',
                            'hessian', 'hs',
                            'hough-transform', 'hough', 'ho',
                        ])

    args = parser.parse_args()

    try:
        cprint('Processing file: ' + str(args.input), 'green')
        image = misc.imread(args.input, flatten=True)

        cprint('Starting ' + args.operation + '!', 'green')

        if args.operation in ['gaussian', 'g']:
            processed = gaussian.filter_image(image, args.gaussian_sigma)

        elif args.operation in ['gradient-magnitude', 'grad-mag', 'gm']:
            processed = gaussian.filter_image(image, args.gaussian_sigma)
            if args.threshold is not None:
                processed = threshold_image(processed, args.threshold)
            else:
                processed = threshold_image(processed)

        elif args.operation in ['edges', 'canny']:
            if args.threshold is not None:
                processed = canny.detect(image, args.gaussian_sigma, args.threshold)
            else:
                processed = canny.detect(image, args.gaussian_sigma)

        elif args.operation in ['ransac', 'r']:
            processed = ransac.detect(image)

        elif args.operation in ['hessian', 'hs']:
            if args.threshold is not None:
                processed, points = hessian.detect(image, threshold=args.threshold, gaus_sig=args.gaussian_sigma)
            else:
                processed, points = hessian.detect(image, gaus_sig=args.gaussian_sigma)

        elif args.operation in ['hough-transform', 'hough', 'ho']:
            processed = hough.detect(image)

    except FileNotFoundError:
        cprint("Can't load image file: " + str(args.input), 'red')
        sys.exit(1)
    except Exception as ex:
        raise ex  # For Development
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
        # default to the format [operation].[original filename].[original extension]
        out_path = './' + args.operation + '.' + input_filename

    # misc.imshow(processed)
    misc.imsave(out_path, processed)


if __name__ == '__main__':
    main()
