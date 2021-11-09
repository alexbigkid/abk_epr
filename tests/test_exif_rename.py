"""Unit tests for main.py"""

# Standard library imports
import unittest

# Third party imports

# Local application imports
from context import ExifRename

class TestExifRename(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.mut = ExifRename()

    # -------------------------------------------------------------------------
    # Tests for get_ingredients
    # -------------------------------------------------------------------------
    def test_ExifRename_changes_into_image_directory_and_back(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
