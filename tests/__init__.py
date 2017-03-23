
import glob, os

dir_path = os.path.dirname(os.path.realpath(__file__))
test_images_dir_path = dir_path + '/images/'
test_images_list = glob.glob(test_images_dir_path + '*')

test_images_dict = {}
for image_path in test_images_list:
    image_dir, image_filename = os.path.split(image_path)
    test_images_dict[image_filename] = image_path

results_dir = os.path.abspath(dir_path + '/../results')
