import os
import pytest
from pathlib import Path
from os import system as cli

# the simplest the better
# globals into the lowest category
# then start climbing


@pytest.fixture
def tmp_file(tmp_path):
    CONTENT = "Destination Demoted!"
    x = tmp_path / "tmp_file.txt"
    x.write_text(CONTENT)
    return x


def EXEC_ARCHIVE():
    cli("./emerch --dry")


# TODO: how to check exit status
def test_exit_01(tmp_file):
    assert True, "exit 01"


def test_archived_exists(tmp_path):
    ARCHIVED = "./archived/"
    archived = tmp_path / Path(ARCHIVED)
    EXEC_ARCHIVE()
    assert archived.is_dir()


def test_move_into_archive(tmp_file):
    print(f"{tmp_file}")
    EXEC_ARCHIVE()
    # run on target
    # check existence
    assert False
