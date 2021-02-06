import sys
import pytest
from pathlib import Path

TEST_DIR = Path(__file__).parent
sys.path.append(f"{TEST_DIR.parent / Path('src')}")

from spacelogger import SpaceLogger


# def test_directory_creation():
#     """Tests the logging file's directory creation abilities.
#     """
# 
#     # Remove any logging directory that might already exist here.
#     dir_path = TEST_DIR / Path("test_dir")
#     test_logger = SpaceLogger("%N $L @ %T", logger_directory=dir_path)
# 
#     if dir_path.exists():
#         dir_path.rmdir()

def test_names():
    """Tests the validity of file names.
    """

    dir_path = TEST_DIR / Path("test_dir")
    test_logger = SpaceLogger("%N $L @ %T")
    test_logger

