import os
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from interfaces.cli import app

runner = CliRunner()


@pytest.fixture
def test_data_dir():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "test_data", "test_dir"
    )


@pytest.fixture
def test_data_wrong_dir():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "test_data",
        "test_dir_wrong_files",
    )


@patch(
    "interfaces.cli.imgly_cli.controller",
)
def test_upload_file_command(mock_controller, test_data_dir):
    result = runner.invoke(app, ["upload-directory", str(test_data_dir)])
    assert result.exit_code == 0
    assert "Uploading" in result.stdout
    assert "to GitHub" in result.stdout
    assert "was successfully uploaded to GitHub" in result.stdout


def test_upload_file_command_file_not_found():
    result = runner.invoke(app, ["upload-directory", "non_existent_file"])
    assert result.exit_code == 1
    assert "Error" in result.stdout
    assert "does not exist" in result.stdout


def test_wrong_directory(test_data_wrong_dir):
    assert os.path.exists(test_data_wrong_dir)
    result = runner.invoke(app, ["upload-directory", str(test_data_wrong_dir)])
    assert result.exit_code == 1
    assert "not supported" in result.stdout
    assert ".xzy" in result.stdout
