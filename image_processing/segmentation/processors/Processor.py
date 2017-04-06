""" A basic outline for an image processor
"""

from termcolor import cprint
from image_processing.utils import bw_to_rgb, cprint_progressbar


class Processor:
    def __init__(self, image, cli_args=None):
        if cli_args is not None and cli_args.verbose:
            self.verbose = cli_args.verbose
        else:
            self.verbose = False

        if image.ndim == 2:
            # Change bw to rgb
            image = bw_to_rgb(image)

        self.image = image.astype('int32')

    def process(self):
        pass

    def get_file_prefix(self):
        return 'processed'

    def print_info(self):
        max_y, max_x, _ = self.image.shape
        cprint('Info:', 'cyan')
        cprint('Image width x height: %d x %d' % (max_x, max_y))
        cprint('Total points: ' + str(max_x * max_y))


class ClusterProcessor(Processor):
    def __init__(self, image, cli_args=None):
        super(ClusterProcessor, self).__init__(image, cli_args=cli_args)
        self.clusters = []

    def add_cluster(self, cluster):
        self.clusters.append(cluster)

    def reset_cluster_vecs(self):
        for cluster in self.clusters:
            cluster.reset_vecs()

    def recenter_clusters(self):
        centers_have_changed = False
        num_changed = 0
        for i in range(len(self.clusters)):
            if self.verbose:
                cprint_progressbar(i, len(self.clusters) - 1, prefix='Clusters Centered:')

            changed = self.clusters[i].recenter()

            if changed:
                num_changed += 1

            # If any cluster has changed centers, report True
            centers_have_changed = changed | centers_have_changed

        if self.verbose:
            cprint('Number of changed centers: ' + str(num_changed), 'yellow')

        return num_changed
