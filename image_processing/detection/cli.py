"""
The command line interface
"""
import argparse
import os
import sys

from scipy import misc
from termcolor import cprint

from image_processing import __version__
from image_processing.operations import gaussian, canny, ransac, hessian, hough
from image_processing.operations.suppression import threshold_image


def main():
    """The exported main function
    
    :return: 
    """
    parser = argparse.ArgumentParser(description='Image detection for cs 558')
    parser.add_argument('-v', '--version', action='version', version=__version__)

    parser.add_argument('-i', '--input', help="The input image to process.", required=True, type=str)
    parser.add_argument('-o', '--output', help="Where to put the output.", type=str)

    parser.add_argument('-gs', '--gaussian-sigma', help="Sigma for gaussian filter.", default=1, type=int)
    parser.add_argument('-t', '--threshold', help="Threshold for various suppression.", type=int)
    parser.add_argument('-it', '--inlier-threshold', help="Inlier threshold for RANSAC suppression.", type=int)
    parser.add_argument('-mi', '--min-inliers', help="Minimum acceptable inliers for RANSAC.", type=int)

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
    operation = ''
    try:
        cprint('Processing file: ' + str(args.input), 'green')
        image = misc.imread(args.input, flatten=True)

        if args.operation in ['gaussian', 'g']:
            operation = 'gaussian'
            cprint('Starting ' + operation + '!', 'green')
            processed = gaussian.filter_image(image, args.gaussian_sigma)

        elif args.operation in ['gradient-magnitude', 'grad-mag', 'gm']:
            operation = 'gradient-magnitude'
            cprint('Starting ' + operation + '!', 'green')
            processed = gaussian.filter_image(image, args.gaussian_sigma)
            if args.threshold is not None:
                processed = threshold_image(processed, args.threshold)
            else:
                processed = threshold_image(processed)

        elif args.operation in ['edges', 'canny']:
            operation = 'canny'
            cprint('Starting ' + operation + '!', 'green')
            if args.threshold is not None:
                processed = canny.detect(image, args.gaussian_sigma, args.threshold)
            else:
                processed = canny.detect(image, args.gaussian_sigma)

        elif args.operation in ['ransac', 'rn']:
            operation = 'ransac'
            cprint('Starting ' + operation + '!', 'green')
            if args.min_inliers is not None:
                processed = ransac.detect(image, min_inliers=args.min_inliers, gaus_sig=args.gaussian_sigma)
            else:
                processed = ransac.detect(image, gaus_sig=args.gaussian_sigma)

        elif args.operation in ['hessian', 'hs']:
            operation = 'hessian'
            cprint('Starting ' + operation + '!', 'green')
            if args.threshold is not None:
                processed, points = hessian.detect(image, threshold=args.threshold, gaus_sig=args.gaussian_sigma)
            else:
                processed, points = hessian.detect(image, gaus_sig=args.gaussian_sigma)

        elif args.operation in ['hough-transform', 'hough', 'ho']:
            operation = 'hough-transform'
            if args.threshold is not None:
                processed = hough.detect(image, feature_threshold=args.threshold, gaus_sig=args.gaussian_sigma)
            else:
                processed = hough.detect(image, gaus_sig=args.gaussian_sigma)

    except FileNotFoundError:
        cprint("Can't load image file: " + str(args.input), 'red')
        sys.exit(1)
    except KeyboardInterrupt:
        cprint('Quitting before save!', 'red')
        sys.exit(0)
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
        # default to the format [operation].[original filename].[original extension]
        prefix = './' + operation + '.' + 'gs-' + str(args.gaussian_sigma) + '.'
        if args.threshold is not None:
            prefix += 't-' + str(args.threshold) + '.'

        out_path = prefix + input_filename

    cprint('Saving to: ' + out_path, 'green')

    # misc.imshow(processed)
    misc.imsave(out_path, processed)


if __name__ == '__main__':
    main()
