"""Constants for spacelogger. Contains color constants, and more.
"""

import colorama

RESET = colorama.Fore.RESET
DEBUG = colorama.Fore.WHITE
SUCCESS = colorama.Fore.GREEN
INFO = colorama.Fore.LIGHTBLACK_EX
WARNING = colorama.Fore.LIGHTYELLOW_EX
CRITICAL = colorama.Fore.LIGHTRED_EX

INVALID_NAME = "^\s+"

conversion_table = {
    DEBUG: "DEBUG",
    INFO: "INFO",
    SUCCESS: "SUCCESS",
    WARNING: "WARNING",
    CRITICAL: "CRITICAL"
}
