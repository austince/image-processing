"""
The command line interface
"""
import argparse
import os
import sys

from scipy import misc
from termcolor import cprint

from . import __version__
from . import processors


def main():
    """The exported main function
    :return: 
    """
    parser = argparse.ArgumentParser(description='Image image_processing for cs 558')
    parser.add_argument('-v', '--version', action='version', version=__version__)

    parser.add_argument('-i', '--input', help="The input image to process.", required=True, type=str)
    parser.add_argument('-o', '--output', help="Where to put the output.", type=str)

    parser.add_argument('-gs', '--gaussian-sigma', help="Sigma for gaussian filter.", default=1, type=int)

    parser.add_argument('-op', '--operation', help="The operation to return.", required=True, type=str,
                        choices=[
                            'k-means', 'k',
                            'SLIC', 'slic', 's'
                        ])

    args = parser.parse_args()
    operation = ''
    processor = processors.Processor()
    try:
        cprint('Processing file: ' + str(args.input), 'green')
        image = misc.imread(args.input)

        if args.operation in ['k-means', 'k']:
            operation = 'k-means'
            processor = processors.Kmeans(image)
        elif args.operation in ['SLIC', 'slic', 's']:
            operation = 'SLIC'
            processor = processors.Slic()

        cprint('Starting ' + operation + '!', 'green')
        processed = processor.process()

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
        prefix = './' + operation + '.' + 'gs-' + str(args.gaussian_sigma) + '.'

        out_path = prefix + input_filename

    cprint('Saving to: ' + out_path, 'green')

    # misc.imshow(processed)
    misc.imsave(out_path, processed)


if __name__ == '__main__':
    main()
