import os
from pathlib import Path

import pytest

from utils import gen_naming_scheme, get_cliparser

PROGRAM = Path("./archive").resolve()
ARCHIVED = Path("archived/")
DAY = Path(gen_naming_scheme())
CONTENT = "Destination Demoted!"
PARSER = get_cliparser()


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


@pytest.fixture
def destination(tmp_path):
    return tmp_path / ARCHIVED / DAY


# @pytest.mark.skip(reason="how to send the correct error?")
# printing the help exists on 0, if this desired behavior
# https://stackoverflow.com/questions/55014222/what-are-response-codes-for-256-and-512-for-os-system-in-python-scripting
def test_exit_with_no_args():
    assert os.system(f"{PROGRAM}") == 0


# pytest.mark.skip(reason="wip")
def test_parser_typings():
    args = PARSER.parse_args([])

    assert args.targets == list()
    assert args.unarchive is False
    assert args.dry is False

    args = PARSER.parse_args("-d -u".split())

    assert args.targets == list()
    assert args.dry is True
    assert args.unarchive is True

    args = PARSER.parse_args("--dry hello world".split())

    assert args.targets == ["hello", "world"]
    assert args.dry is True
    assert args.unarchive is False


def test_robustness_against_empty_string():
    assert os.system(f"{PROGRAM} ''") == 0


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


def test_target_arrives_at_correct_destination(tmp_path, gen_tmp_files, destination):
    (tmp_file,) = gen_tmp_files(1)
    os.chdir(tmp_path)
    os.system(f"{PROGRAM} {tmp_file}")

    assert destination.exists(), "destination NOT exists"
    assert (destination / tmp_file.name).exists(), "INcorrect target destination"


def test_unarchive(tmp_path, gen_tmp_files):
    (tmp_file,) = gen_tmp_files(1)
    os.chdir(tmp_path)
    assert tmp_file.exists()

    os.system(f"{PROGRAM} {tmp_file}")

    os.system(f"{PROGRAM} --unarchive")

    # Is unarchived
    assert tmp_file.exists()


# Random chain of creations and destructions
# It is a good idea
def test_no_empty_directories(tmp_path, gen_tmp_files, destination):
    (f1, f2) = gen_tmp_files(2)
    os.chdir(tmp_path)

    os.system(f"{PROGRAM} {f1}")
    os.system(f"{PROGRAM} {f2}")

    assert not f2.exists()

    os.system(f"{PROGRAM} -u")
    # f2 returns
    assert destination.exists()
    # assert set(os.listdir(str(destination))) == set(['f1'])
    # assert f2.exists()

    # f1 returns
    # os.system(f"{PROGRAM} -u")
    # assert not destination.exist()


def test_name_collisions(tmp_path, gen_tmp_files, destination):
    (tmp_file1, tmp_file2, tmp_file3) = gen_tmp_files(3)

    os.chdir(tmp_path)

    # First the cointaining directory has to be created
    block_dir = destination / tmp_file2.name
    block_dir.mkdir(parents=True)

    block_file = destination / tmp_file1.name
    block_file.write_text(CONTENT)

    # shutil.Error
    # triggers exit code 256
    # same name file is catched by exceptions
    assert os.system(f"{PROGRAM} {tmp_file1}") == 0
    # same name dir is catched by exceptions
    assert os.system(f"{PROGRAM} {tmp_file2}") == 0

    os.system(f"rm -r {destination}")
    assert not destination.exists()
    block_day = "." / ARCHIVED / DAY.name
    block_day.write_text(CONTENT)

    out = os.system(f"{PROGRAM} {tmp_file3}")

    assert tmp_file3.exists()
    assert block_day.is_file()
    assert out == 0
