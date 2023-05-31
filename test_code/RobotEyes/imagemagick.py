import subprocess

from robot.api import logger


class Imagemagick(object):

    def __init__(self, img1, img2, diff):
        self.img1 = img1
        self.img2 = img2
        self.diff = diff

    def compare_images(self):
        compare_cmd = 'compare -metric RMSE -subimage-search -dissimilarity-threshold 1.0 "%s" "%s" "%s"' \
                      % (self.img1, self.img2, self.diff)

        attempts = 0
        logger.debug(f'Comparing image: {compare_cmd}')
        while attempts < 2:
            proc = subprocess.Popen(compare_cmd,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            out, err = proc.communicate()
            logger.debug('Comparison output: %s' % err)
            diff = err.split()[1][1:-1]

            try:
                trimmed = float("{:.2f}".format(float(diff)))
                return trimmed
            except ValueError:
                if attempts == 0:
                    logger.debug('Comparison failed first time. Output %s' % err)
                    compare_cmd = 'magick ' + compare_cmd
                else:
                    raise Exception('Could not parse comparison output: %s' % err)
            finally:
                attempts += 1
