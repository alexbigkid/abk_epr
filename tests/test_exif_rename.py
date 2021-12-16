"""Unit tests for main.py"""

# Standard library imports
import unittest
import logging
import logging.config
from unittest.mock import patch, call

# Third party imports
from optparse import OptionParser, Values

# Local application imports
from context import ExifRename

class TestExifRename(unittest.TestCase):
    TEST_IMAGE_DIR = './unittest_image_dir'
    TEST_CURRENT_DIR = './unittest_current_dir'
    _current_dir = None

    def setUp(self) -> None:
        self.maxDiff = None
        values = Values()
        values.dir = self.TEST_IMAGE_DIR
        values.verbose = False
        values.log_into_file = False
        self.mut = ExifRename(options=values)
        return super().setUp()


    # -------------------------------------------------------------------------
    # Tests for get_ingredients
    # -------------------------------------------------------------------------
    def test_ExifRename__setup_logger_throws_given_yaml_config_file_does_not_exist(self):
        with self.assertRaises(IOError) as context:
            self.mut._options.config_log_file = 'NotValidFile.yaml'
            self.mut._setup_logging()
        self.assertEqual('NotValidFile.yaml does not exist.', str(context.exception))


    # def test_ExifRename_changes_into_image_directory_and_back(self):
    #     # logger = logging.getLogger(ExifRename.LOG_CONFIG_FILE)
    #     with patch.object(logging.config, 'getLogger') as mock_getLogger:
    #         with patch.object(logging, 'debug') as mock_logging_debug:
    #             self.mut.handle_options()
    #             self.assertEqual(mock_getLogger.mock_calls, [call(ExifRename.LOG_CONFIG_FILE)])
    #             self.assertEqual(mock_logging_debug.mock_calls, [call("logger_type: consoleLogger")])
    #         # with patch('os.getcwd', return_value=self.TEST_CURRENT_DIR) as mock_getcwd:
    #         #     with patch('os.chdir') as mock_chdir:
    #         #         self.mut.move_rename_convert_images()
    #         #         self.assertEqual(mock_getcwd.mock_calls, [call()])
    #         #         self.assertEqual(mock_chdir.mock_calls, [call(self.TEST_IMAGE_DIR), call(self.TEST_CURRENT_DIR)])


if __name__ == '__main__':
    unittest.main()
