#!/usr/bin/env python
"""Main program for renaming images and translate images from raw to dng format"""

# Standard library imports
import sys
# import asyncio

# Third party imports
from optparse import OptionParser
from pydngconverter import DNGConverter, flags
from colorama import Fore, Style
# import exiftool

# Local application imports
from _version import __version__

class ExifRename:
    """ExifRename contains module to convert RAW images to DNG and rename them using exif meta data"""

    _options = None
    _args = None

    def handle_options(self):
        usage_string = "usage: %prog [options]"
        version_string = "%prog version: " + Fore.GREEN + f"{__version__}{Style.RESET_ALL}"
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
        (self._options, self._args) = parser.parse_args()

        if len(self._args) != 0:
            parser.error("wrong number of arguments")

        if self._options.verbose:
            print(f"options: {self._options}")
            print(f"args: {self._args}")
            print(f"options.dir: {self._options.dir}")
            print(f"__version__: {__version__}")

def main():
    exit_code = 0

    try:
        exif_rename = ExifRename()
        exif_rename.handle_options()
    except Exception as exception:
        print(Fore.RED + f"ERROR: executing exif image renamer")
        print(f"{exception}{Style.RESET_ALL}")
        exit_code = 1
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
