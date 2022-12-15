import pytest
import os

# the simplest the better
# globals into the lowest category
# then start climbing

@pytest.fixture
def tmp_file(tmp_path):
    CONTENT = "Destination Demoted!"
    x = tmp_path / "tmp_file.txt"
    x.write_text(CONTENT)
    return x


def test_exit_01(tmp_file):
    print(f"{tmp_file}\n {type(tmp_file)}")
    assert False, "exit 01"


def test_archived_exists(tmp_file):
    print(f"{tmp_file}")
    ARCHIVED = "./archived/"
    assert False, "archived_exists"


def test_move_into_archive(tmp_file):
    print(f"{tmp_file}")
    # run on target
    # check existence
