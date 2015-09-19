import json
import os
import unittest

from url import APP_ROOT, IMAGES, IMAGE_PATH


class TestImages(unittest.TestCase):

    def test_all_images_exist(self):
        for image in IMAGES.keys():
            image_path = os.path.join(IMAGE_PATH, image)
            self.assertTrue(os.path.isfile(image_path), 'Missing image: %s' % image_path)

    def test_no_extra_images_exist(self):
        for image in os.listdir(IMAGE_PATH):
            if image in ['.DS_Store']:
                continue
            self.assertIn(image, IMAGES.keys(), "Found extra image file: %s" % image)


if __name__ == '__main__':
    unittest.main()
