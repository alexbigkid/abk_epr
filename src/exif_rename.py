#!/usr/bin/env python
"""Main program for renaming images and translate images from raw to dng format"""

# Standard library imports
import os
import sys
import logging
import logging.config
import yaml
import re
import datetime
import timeit
import json
# import asyncio

# Third party imports
from optparse import OptionParser, Values
# from pydngconverter import DNGConverter, flags
from colorama import Fore, Style
from yaml.loader import Loader
from colorama import Fore, Style
import exiftool

# Local application imports
from _version import __version__


CONSOLE_LOGGER = 'consoleLogger'
FILE_LOGGER = 'fileLogger'


def function_trace(original_function):
    """Decorator function to help to trace function call entry and exit
    Args:
        original_function (_type_): function above which the decorater is defined
    """
    def function_wrapper(*args, **kwargs):
        _logger = logging.getLogger(original_function.__name__)
        _logger.debug(f"{Fore.CYAN}-> {original_function.__name__}{Fore.RESET}")
        result = original_function(*args, **kwargs)
        _logger.debug(f"{Fore.CYAN}<- {original_function.__name__}{Fore.RESET}\n")
        return result
    return function_wrapper


class PerformanceTimer(object):
    def __init__(self, timer_name, logger=None):
        self._timer_name = timer_name
        self._logger = logger
    def __enter__(self):
        self.start = timeit.default_timer()
    def __exit__(self, exc_type, exc_value, traceback):
        time_took = (timeit.default_timer() - self.start) * 1000.0
        self._logger.info('Executing {} took {} ms'.format(self._timer_name, str(time_took)))



class CommandLineOptions(object):
    """CommandLineOptions module handles all parameters passed in to the python script"""
    _args = None
    options = None
    logger = None

    def __init__(self, args:list=None, options:Values=None):
        self._args = args
        self.options = options
        self.logger = None


    def handle_options(self) -> None:
        """Handles user specified options and arguments"""
        usage_string = "usage: %prog [options]"
        version_string = f"%prog version: {Fore.GREEN}{__version__}{Style.RESET_ALL}"
        parser = OptionParser(usage=usage_string, version=version_string)
        parser.add_option(
            "-d",
            "--directory",
            action="store",
            dest="dir",
            default=".",
            help="directory, where images will be converted and renamed"
        )
        parser.add_option(
            "-v",
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="verbose execution"
        )
        parser.add_option(
            "-l",
            "--log_into_file",
            action="store_true",
            dest="log_into_file",
            default=False,
            help="log into file exif_rename.log if True, otherwise log into console"
        )
        parser.add_option(
            "-c",
            "--config_log_file",
            action="store",
            dest="config_log_file",
            default="./src/logging.yaml",
            help="config file for logging print outs"
        )
        (self.options, self._args) = parser.parse_args()

        if len(self._args) != 0:
            parser.error("wrong number of arguments")
        self._setup_logging()
        self.logger.info(f"options: {self.options}")
        self.logger.info(f"args: {self._args}")
        self.logger.info(f"options.dir: {self.options.dir}")
        self.logger.info(f"options.verbose: {self.options.verbose}")
        self.logger.info(f"options.log_into_file: {self.options.log_into_file}")
        self.logger.info(f"__version__: {__version__}")


    def _setup_logging(self) -> None:
        try:
            with open(self.options.config_log_file, 'r') as stream:
                try:
                    config_yaml = yaml.load(stream, Loader=yaml.FullLoader)
                    logging.config.dictConfig(config_yaml)
                    logger_type = (CONSOLE_LOGGER, FILE_LOGGER)[self.options.log_into_file]
                    self.logger = logging.getLogger(logger_type)
                    self.logger.disabled = self.options.verbose == False
                except ValueError:
                    raise ValueError(f'{self.options.config_log_file} is not a valid yaml format')
                except Exception as ex:
                    raise Exception(f'not ValueError: {ex.exeption}')
        except IOError:
            raise IOError(f'{self.options.config_log_file} does not exist.')
        self.logger.debug(f"logger_type: {logger_type}")



class ExifRename(object):
    """ExifRename contains module to convert RAW images to DNG and rename them using exif meta data"""
    FILES_TO_EXCLUDE_EXPRESSION  = 'Adobe Bridge Cache|Thumbs.db|^\.'
    THMB = { "ext": "jpg", "dir": "thmb" }
    SUPPORTED_RAW_EXTENSION = [ '.cr2', '.nef', '.arw' ]
    EXIF_UNKNOWN            = 'unknown'
    EXIF_SOURCE_FILE        = 'SourceFile'
    EXIF_CREATE_DATE        = 'EXIF:CreateDate'
    EXIF_MAKE               = 'EXIF:Make'
    EXIF_MODEL              = 'EXIF:Model'
    EXIF_TAGS = [ EXIF_CREATE_DATE, EXIF_MAKE, EXIF_MODEL ]
    DIR_NAME                = 'DirName'


    def __init__(self, logger:logging.Logger=None, options:Values=None):
        self._logger = logger or logging.getLogger(__name__)
        self._options = options
        self._current_dir = None


    def __del__(self):
        pass
        # if self._options.verbose:
        #     self._logger.


    @function_trace
    def check_exiftool(self) -> None:
        with exiftool.ExifTool() as et:
            et.logger=self._logger
            exiftool_exe = et.executable
            self._logger.debug(f'{exiftool_exe=}')

    @function_trace
    def move_rename_convert_images(self) -> None:
        self._validate_image_dir()
        self._change_to_image_dir()
        metadata_list = self._read_image_dir()
        self._move_and_rename_files()
        self._change_from_image_dir()


    @function_trace
    def return_to_previous_state(self):
        self._change_from_image_dir()


    @function_trace
    def _change_to_image_dir(self) -> None:
        if self._options.dir != ".":
            self._current_dir = os.getcwd()
            os.chdir(self._options.dir)
            self._logger.info(f"inside directory: {self._options.dir}")


    @function_trace
    def _change_from_image_dir(self) -> None:
        if self._current_dir is not None:
            os.chdir(self._current_dir)
            self._logger.info(f"inside directory: {self._current_dir}")


    @function_trace
    def _move_and_rename_files(self) -> None:
        pass


    @function_trace
    def _convert_raw_files(self) -> None:
        pass


    @function_trace
    def _read_image_dir(self) -> list:
        metadata_list = []
        with PerformanceTimer(timer_name="ReadingImageDirectory", logger=self._logger):
            files_list = [f for f in os.listdir('.') if os.path.isfile(f)]
            filtered_list = sorted([i for i in files_list if not re.match(rf'{self.FILES_TO_EXCLUDE_EXPRESSION}', i)])
            self._logger.debug(f"filtered_list = {filtered_list}")
            with exiftool.ExifTool() as et:
                et.logger = self._logger
                metadata_list = et.get_tags_batch(self.EXIF_TAGS, filtered_list)
            if len(metadata_list) > 0:
                for metadata in metadata_list:
                    # detect thumbnail files
                    file_name = metadata.get(self.EXIF_SOURCE_FILE)
                    file_base, file_extension = os.path.splitext(os.path.basename(file_name))
                    file_extension = file_extension.replace('.', '').lower()
                    if file_extension == self.THMB['ext']:
                        # timeit here
                        for raw_ext in self.SUPPORTED_RAW_EXTENSION:
                            # if os.path.isfile(f'{file_base}{raw_ext}'):
                            if f'{file_base.lower()}{raw_ext}' in [ j.lower() for j in filtered_list ]:
                                file_extension = self.THMB['dir']
                                self._logger.debug(f'{file_extension=} for file: {file_name}')
                    # modify the date format
                    metadata[self.EXIF_CREATE_DATE] = metadata.get(self.EXIF_CREATE_DATE, self.EXIF_UNKNOWN).replace(':','').replace(' ','_')
                    metadata[self.EXIF_MAKE] = metadata.get(self.EXIF_MAKE, self.EXIF_UNKNOWN).replace(' ','').lower()
                    metadata[self.EXIF_MODEL] = metadata.get(self.EXIF_MODEL, self.EXIF_UNKNOWN).replace(' ','').lower()
                    dir_name = '_'.join([metadata[self.EXIF_MAKE], metadata[self.EXIF_MODEL], file_extension])
                    metadata[self.DIR_NAME] = dir_name
            else:
                raise Exception('no files to process for current directory.')
            self._logger.debug(f'metadata_list = {json.dumps(metadata_list, indent=4)}')
        return metadata_list


    @function_trace
    def _validate_image_dir(self):
        self._logger.debug(f"self._options.dir: {self._options.dir}")
        try:
            dir_name_to_validate = (self._options.dir, os.getcwd())[self._options.dir == '.']
            last_part_of_dir = os.path.basename(os.path.normpath(dir_name_to_validate))
            date_format = re.match('^(\d{8})_\w+$', last_part_of_dir)
            datetime.datetime.strptime(date_format.group(1), '%Y%m%d')
        except:
            raise Exception("Not a valid date / directory format, please use: YYYYMMDD_name_of_the_project")



def main():
    exit_code = 0

    try:
        command_line_options = CommandLineOptions()
        command_line_options.handle_options()
        exif_rename = ExifRename(logger=command_line_options.logger, options=command_line_options.options)
        exif_rename.check_exiftool()
        exif_rename.move_rename_convert_images()
    except Exception as exception:
        exif_rename.return_to_previous_state()
        print(f"{Fore.RED}ERROR: executing exif image renamer")
        print(f"EXCEPTION: {exception}{Style.RESET_ALL}")
        exit_code = 1
    finally:
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
