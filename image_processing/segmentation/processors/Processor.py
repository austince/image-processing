""" A basic outline for an image processor
"""


class Processor:
    def __init__(self, image, cli_args=None):
        if cli_args is not None and cli_args.verbose:
            self.verbose = cli_args.verbose
        else:
            self.verbose = False

        self.image = image.astype('int32')

    def process(self):
        pass

    def get_file_prefix(self):
        return ''
