import pytest
from pathlib import Path
import os


PROGRAM = Path("./archive").resolve()


@pytest.fixture
def tmp_file(tmp_path):
    CONTENT = "Destination Demoted!"
    x = tmp_path / "tmp_file.txt"
    x.write_text(CONTENT)
    return x


# https://stackoverflow.com/questions/55014222/what-are-response-codes-for-256-and-512-for-os-system-in-python-scripting
def test_exit_with_no_args():
    assert os.system(f"{PROGRAM}") != 0


def test_dry_does_nothing(tmp_file, tmp_path):
    os.chdir(tmp_path)
    os.system(f"{PROGRAM} --dry {tmp_file}")
    assert not (tmp_path / "archived/").exists()


def test_archived(tmp_file, tmp_path):
    os.chdir(tmp_path)
    os.system(f"{PROGRAM} {tmp_file}")
    assert (tmp_path / "archived").exists()
    assert not tmp_file.exists()
    assert ((tmp_path / "archived") / tmp_file.name).exists()
