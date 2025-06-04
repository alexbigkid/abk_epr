"""Cli - entry point to the abk_bwp package."""

import asyncio
from abk_epr import clo
from abk_epr.epr import epr


def main():
    """Main function."""
    command_line_options = clo.CommandLineOptions()
    command_line_options.handle_options()
    asyncio.run(epr())
