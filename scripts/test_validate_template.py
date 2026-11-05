"""Regression checks for silhouette validation; synthetic fixtures only."""
import tempfile
from pathlib import Path
import unittest
from PIL import Image
from validate_template import check


class TemplateChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.template = Image.new('RGBA', (16, 16), (255, 255, 255, 0))
        for x in range(3, 11):
            for y in range(3, 11):
                self.template.putpixel((x, y), (255, 255, 255, 255))
        self.template.putpixel((13, 13), (255, 255, 255, 255))
        self.template.putpixel((2, 3), (255, 255, 255, 64))
        self.template.save(self.root / 'template.png')

    def run_image(self, image):
        image.save(self.root / 'candidate.png')
        return check(self.root / 'template.png', self.root / 'candidate.png')

    def test_artwork_color_is_not_geometry(self):
        image = Image.new('RGBA', (16, 16), (0, 0, 0, 255))
        image.putalpha(self.template.getchannel('A'))
        self.assertTrue(self.run_image(image)['passed'])

    def test_small_island_missing(self):
        image = self.template.copy()
        image.putpixel((13, 13), (255, 255, 255, 0))
        result = self.run_image(image)
        self.assertFalse(result['passed'])
        self.assertEqual(result['missing_opaque_pixels'], 1)

    def test_stray_background_pixel(self):
        image = self.template.copy()
        image.putpixel((0, 0), (0, 255, 0, 1))
        self.assertEqual(self.run_image(image)['spill_pixels'], 1)

    def test_antialias_must_match(self):
        image = self.template.copy()
        image.putpixel((2, 3), (0, 0, 0, 255))
        self.assertFalse(self.run_image(image)['passed'])

    def test_opaque_candidate_fails(self):
        self.assertFalse(self.run_image(self.template.convert('RGB'))['passed'])

    def test_wrong_dimensions(self):
        self.assertFalse(self.run_image(Image.new('RGBA', (8, 8)))['passed'])

    def test_opaque_reference_is_unsupported(self):
        self.template.convert('RGB').save(self.root / 'template.png')
        self.assertIn('no usable alpha', self.run_image(self.template)['errors'][0])


if __name__ == '__main__':
    unittest.main()
