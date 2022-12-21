import os
from pathlib import Path

import pytest

from utils import gen_naming_scheme

PROGRAM = Path("./archive").resolve()
ARCHIVED = Path("archived/")
DAY = gen_naming_scheme()
CONTENT = "Destination Demoted!"


@pytest.fixture
def gen_tmp_files(tmp_path):
    PATH = tmp_path
    SUFFIX = ".txt"

    def x(n=1):

        tmp_files = []

        for i in range(n):
            tmp_file = PATH / (str(i) + SUFFIX)
            tmp_file.write_text(CONTENT)
            tmp_files.append(tmp_file)

        return tmp_files

    return x


# https://stackoverflow.com/questions/55014222/what-are-response-codes-for-256-and-512-for-os-system-in-python-scripting
def test_exit_with_no_args():
    assert os.system(f"{PROGRAM}") != 0


def test_dry_does_nothing(tmp_path, gen_tmp_files):
    (tmp_file,) = gen_tmp_files(1)
    os.chdir(tmp_path)
    os.system(f"{PROGRAM} --dry {tmp_file}")
    assert not (tmp_path / ARCHIVED).exists()


def test_target_is_cleared(tmp_path, gen_tmp_files):
    (tmp_file,) = gen_tmp_files(1)
    os.chdir(tmp_path)
    os.system(f"{PROGRAM} {tmp_file}")

    assert not tmp_file.exists(), "target is NOT cleared"


def test_target_arrives_at_correct_destination(tmp_path, gen_tmp_files):
    (tmp_file,) = gen_tmp_files(1)
    os.chdir(tmp_path)
    os.system(f"{PROGRAM} {tmp_file}")

    destination = tmp_path / ARCHIVED / DAY

    assert destination.exists(), "destination NOT exists"
    assert (destination / tmp_file.name).exists(), "INcorrect target destination"


def test_name_collisions(tmp_path, gen_tmp_files):
    (tmp_file1, tmp_file2) = gen_tmp_files(2)

    os.chdir(tmp_path)

    destination = tmp_path / ARCHIVED / DAY

    block_dir = destination / tmp_file2.name
    block_dir.mkdir(parents=True)

    block_file = destination / tmp_file1.name
    block_file.write_text(CONTENT)

    # Why is not working, cause is not level 1???

    # dir blocking
    # import shutil
    # with pytest.raises(shutil.SameFileError):
    #     os.system(f"{PROGRAM} {tmp_file1}")

    # file blocking
    # with pytest.raises(FileExistsError):
    #     os.system(f"{PROGRAM} {tmp_file2}")

    os.system(f"{PROGRAM} {tmp_file1}")
    os.system(f"{PROGRAM} {tmp_file2}")
