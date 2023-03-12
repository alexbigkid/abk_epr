"""Unit tests for main.py"""

# Standard library imports
import unittest
import logging
import logging.config
from unittest.mock import mock_open, patch, call

# Third party imports
from optparse import OptionParser, Values
from parameterized import parameterized

# Local application imports
from context import CommandLineOptions, ExifRename

class TestExifRename(unittest.TestCase):
    TEST_IMAGE_DIR = './20220101_unittest_image_dir'
    TEST_CURRENT_DIR = './20220101_unittest_current_dir'
    _current_dir = None
    yaml_file = """version: 1
disable_existing_loggers: True
formatters:
    abkFormatterShort:
        format: '[%(asctime)s]:[%(funcName)s]:[%(levelname)s]: %(message)s'
        datefmt: '%Y%m%d %H:%M:%S'
handlers:
    consoleHandler:
        class: logging.StreamHandler
        level: DEBUG
        formatter: abkFormatterShort
        stream: ext://sys.stdout
loggers:
    consoleLogger:
        level: DEBUG
        handlers: [consoleHandler]
        qualname: consoleLogger
        propagate: no
"""
    mut = None


    def setUp(self) -> None:
        self.maxDiff = None
        values = Values()
        values.dir = self.TEST_IMAGE_DIR
        values.verbose = False
        values.log_into_file = False
        self.clo = CommandLineOptions()
        self.clo.options = values
        return super().setUp()

    # -------------------------------------------------------------------------
    # Tests for CommandLineOptions
    # -------------------------------------------------------------------------
    def test_CommandLineOptions__setup_logger_throws_given_yaml_config_file_does_not_exist(self) -> None:
        with self.assertRaises(IOError) as context:
            self.clo.options.config_log_file = 'NotValidFile.yaml'
            self.clo._setup_logging()
        self.assertEqual(str(context.exception), "[Errno 2] No such file or directory: 'NotValidFile.yaml'")


    def test_CommandLineOptions__setup_logger_throws_given_invalid_yaml_file(self) -> None:
        with patch("builtins.open", mock_open(read_data='{"notValid": 2}')) as mock_file:
            with self.assertRaises(ValueError) as context:
                self.clo.options.config_log_file = 'valid.yaml'
                self.clo._setup_logging()
            self.assertEqual(str(context.exception), 'valid.yaml is not a valid yaml format')
            mock_file.assert_called_with('valid.yaml', 'r', encoding='utf-8')


    # -------------------------------------------------------------------------
    # Tests for ExifRename
    # -------------------------------------------------------------------------
    @parameterized.expand([
        './NODATE_unittest_image_dir',
        '/blah-blah/INVALID_DIR_FORMAT_20220101_unittest_image_dir/',
        '../data/20220101NO_UNDERSCORE_DIR',
        '020221301_TOO_MANY_DIGITS',
        '0221301_NOT_ENOUGH_DIGITS',
        '00000101_INVALID_YEAR',
        '20221301_INVALID_MONTH',
        '20220132_INVALID_DAY',
        '20220229_INVALID_DAY_NOT_LEAP_YEAR',
    ])
    def test_ExifRename__move_rename_convert_images_throws_given_image_dir_has_invalid_format(self, image_dir:str) -> None:
        with patch("builtins.open", mock_open(read_data=self.yaml_file)) as mock_file:
            self.clo.options.config_log_file = 'valid.yaml'
            self.clo.options.dir = image_dir
            self.clo._setup_logging()
            mock_file.assert_called_with('valid.yaml', 'r', encoding='utf-8')
            self.mut = ExifRename(logger=self.clo.logger, options=self.clo.options)
            with patch('os.getcwd') as mock_getcwd:
                with patch('os.chdir') as mock_chdir:
                    with patch('os.listdir') as mock_listdir:
                        with self.assertRaises(Exception) as context:
                            self.mut.move_rename_convert_images()
                        self.assertEqual(
                            f"Not a valid date / directory format, please use: YYYYMMDD_name_of_the_project",
                            str(context.exception)
                        )
                    self.assertEqual(mock_listdir.mock_calls, [])
                self.assertEqual(mock_chdir.mock_calls, [])
            self.assertEqual(mock_getcwd.mock_calls, [call()])


    def test_ExifRename__move_rename_convert_images_throws_given_image_dir_does_not_exist(self) -> None:
        with patch("builtins.open", mock_open(read_data=self.yaml_file)) as mock_file:
            self.clo.options.config_log_file = 'valid.yaml'
            self.clo._setup_logging()
            mock_file.assert_called_with('valid.yaml', 'r', encoding='utf-8')
            self.mut = ExifRename(logger=self.clo.logger, options=self.clo.options)
            with patch('os.getcwd', return_value=self.TEST_CURRENT_DIR) as mock_getcwd:
                with patch('os.chdir', side_effect=Exception(f"No such file or directory: '{self.TEST_IMAGE_DIR}'")) as mock_chdir:
                    with self.assertRaises(Exception) as context:
                        self.mut.move_rename_convert_images()
                    self.assertEqual(f"No such file or directory: '{self.TEST_IMAGE_DIR}'", str(context.exception))
                self.assertEqual(mock_chdir.mock_calls, [call(self.TEST_IMAGE_DIR)])
            self.assertEqual(mock_getcwd.mock_calls, [call(), call()])


    @unittest.skip("test not ready")
    def test_ExifRename__move_rename_convert_images_does_not_change_dir_given_it_is_current_dir(self) -> None:
        with patch("builtins.open", mock_open(read_data=self.yaml_file)) as mock_file:
            self.clo.options.config_log_file = 'valid.yaml'
            self.clo.options.dir = '.'
            self.clo._setup_logging()
            mock_file.assert_called_with('valid.yaml', 'r', encoding='utf-8')
            self.mut = ExifRename(logger=self.clo.logger, options=self.clo.options)
            with patch('os.getcwd', return_value=self.TEST_CURRENT_DIR) as mock_getcwd:
                with patch('os.chdir') as mock_chdir:
                    files_to_return = ['a.json', 'b.json', 'c.json', 'd.txt']
                    with patch('os.listdir', return_value=files_to_return) as mock_listdir:
                        self.mut.move_rename_convert_images()
                    self.assertEqual(mock_listdir.mock_calls, [call('.')])
                self.assertEqual(mock_chdir.mock_calls, [])
            self.assertEqual(mock_getcwd.mock_calls, [call()])

    @unittest.skip("test not ready")
    def test_ExifRename__move_rename_convert_images_calls_get_change_list_dir(self) -> None:
        with patch("builtins.open", mock_open(read_data=self.yaml_file)) as mock_file:
            self.clo.options.config_log_file = 'valid.yaml'
            self.clo._setup_logging()
            mock_file.assert_called_with('valid.yaml', 'r', encoding='utf-8')
            self.mut = ExifRename(logger=self.clo.logger, options=self.clo.options)
            with patch('os.getcwd', return_value=self.TEST_CURRENT_DIR) as mock_getcwd:
                with patch('os.chdir') as mock_chdir:
                    files_to_return = ['a.json', 'b.json']
                    with patch('os.listdir', return_value=files_to_return) as mock_listdir:
                        with patch('os.path.isfile', return_value=True) as mock_isfile:
                            self.mut.move_rename_convert_images()
                        self.assertEqual(mock_isfile.mock_calls, [call(files_to_return[0]), call(files_to_return[1])])
                    self.assertEqual(mock_listdir.mock_calls, [call('.')])
                self.assertEqual(mock_chdir.mock_calls, [call(self.TEST_IMAGE_DIR), call(self.TEST_CURRENT_DIR)])
            self.assertEqual(mock_getcwd.mock_calls, [call(), call()])


if __name__ == '__main__':
    unittest.main()
