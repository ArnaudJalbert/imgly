import os
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from interfaces.cli import app

runner = CliRunner()


@pytest.fixture
def test_data_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test_data")


@patch(
    "interfaces.cli.imgly_cli.controller",
)
def test_upload_file_command(mock_controller, test_data_dir):
    file_path = Path(os.path.join(test_data_dir, "img.png"))
    result = runner.invoke(app, ["upload-file", str(file_path)])
    assert result.exit_code == 0, print(result.stdout)
    mock_controller.upload_media.assert_called_once()
    assert "Uploading" in result.stdout
    assert "successfully uploaded" in result.stdout
    assert file_path.name in result.stdout


def test_upload_file_command_file_not_exist(test_data_dir):
    file_path = Path(os.path.join(test_data_dir, "img2.png"))
    result = runner.invoke(app, ["upload-file", str(file_path)])
    assert result.exit_code == 1
    assert "does not exist." in result.stdout
    assert str(file_path.name) in result.stdout


def test_upload_file_command_bad_extension(test_data_dir):
    file_path = Path(os.path.join(test_data_dir, "img.HEIC"))
    result = runner.invoke(app, ["upload-file", str(file_path)])
    assert result.exit_code == 1
    assert "is not a supported image type." in result.stdout
