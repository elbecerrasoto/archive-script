import pytest
from pathlib import Path
import os


def gen_naming_scheme():
    return "today"


PROGRAM = Path("./archive").resolve()
ARCHIVED = Path("archived/")
DAY = gen_naming_scheme()


@pytest.fixture
def tmp_file(tmp_path):
    CONTENT = "Destination Demoted!"
    x = tmp_path / "tmp_file.txt"
    x.write_text(CONTENT)
    return x


# https://stackoverflow.com/questions/55014222/what-are-response-codes-for-256-and-512-for-os-system-in-python-scripting
def test_exit_with_no_args():
    assert os.system(f"{PROGRAM}") != 0


def test_dry_does_nothing(tmp_path, tmp_file):
    os.chdir(tmp_path)
    os.system(f"{PROGRAM} --dry {tmp_file}")
    assert not (tmp_path / ARCHIVED).exists()


def test_target_is_cleared(tmp_path, tmp_file):
    os.chdir(tmp_path)
    os.system(f"{PROGRAM} {tmp_file}")

    assert not tmp_file.exists(), "! target is cleared"


def test_target_arrives_at_correct_destination(tmp_path, tmp_file):
    os.chdir(tmp_path)
    os.system(f"{PROGRAM} {tmp_file}")

    destination = tmp_path / DAY / ARCHIVED
    # assert assert_correct_naming_scheme(day)

    assert destination.exists(), "! destination exists"
    assert destination / tmp_file.name.exists(), "! correct target destination"
