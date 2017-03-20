import argparse
import os
import sys

from scipy import misc
from termcolor import cprint

from detection import __version__
from detection.operations import gaussian, edges, ransac, hessian, hough
from detection.operations.suppression import threshold_image


def main():
    parser = argparse.ArgumentParser(description='Image detection for cs 558')
    parser.add_argument('-v', '--version', action='version', version=__version__)

    parser.add_argument('-i', '--input', help="The input image to process.", required=True, type=str)
    parser.add_argument('-o', '--output', help="Where to put the output.", default=None, type=str)

    parser.add_argument('-gs', '--gaussian-sigma', help="Sigma for gaussian filter", default=1, type=int)
    parser.add_argument('-t', '--threshold', help="Threshold for non max suppression", default=100, type=int)

    parser.add_argument('-op', '--operation', help="The operation to return.", required=True, type=str,
                        choices=[
                            'gaussian',
                            'gradient-magnitude', 'grad-mag',
                            'edges',
                            'ransac',
                            'hessian',
                            'hough-transform', 'hough',
                        ])

    args = parser.parse_args()

    try:
        cprint('Processing file: ' + str(args.input), 'green')
        image = misc.imread(args.input, flatten=True)

        cprint('Starting ' + args.operation + '!', 'green')

        if args.operation == 'gaussian':
            processed = gaussian.filter_image(image, args.gaussian_sigma)
        elif args.operation == 'gradient-magnitude' or args.operation == 'grad-mag':
            processed = gaussian.filter_image(image, args.gaussian_sigma)
            processed = threshold_image(processed, args.threshold)
        elif args.operation == 'edges':
            processed = edges.detect(image, args.gaussian_sigma, args.threshold)
        elif args.operation == 'ransac':
            processed = ransac.detect(image)
        elif args.operation == 'hessian':
            processed = hessian.detect(image, gaus_sig=args.gaussian_sigma)
        elif args.operation == 'hough-transform' or args.operation == 'hough':
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
        out_path = './' + args.operation + '.' + input_filename

    # misc.imshow(processed)
    misc.imsave(out_path, processed)


if __name__ == '__main__':
    main()
