""" A basic outline for an image processor
"""


class Processor:
    def __init__(self, cli_args=None):
        if cli_args is not None and cli_args.verbose:
            self.verbose = cli_args.verbose
        else:
            self.verbose = False

    def process(self):
        pass
