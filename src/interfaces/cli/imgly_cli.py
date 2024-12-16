import base64
from pathlib import Path
from typing import Optional, Set

import typer

from rich import print

from imgly.constants import SUPPORTED_IMAGES_EXTENSIONS
from imgly import ImglyController
from imgly.infra.github_infrastructure import (
    GitHubRepository,
    DuplicateMediaError,
    UploadMediaError,
)

app: typer.Typer = typer.Typer()
github_repository: GitHubRepository = GitHubRepository()
controller: ImglyController = ImglyController(repository=github_repository)


@app.command()
def upload_file(
    file_path: str, description: Optional[str] = typer.Argument(default=None)
) -> None:
    """
    Uploads a file to the set Repository.

    Args:
        file_path: The path to the file to upload.
        description: An optional description for the file.

    Raises:
        typer.Abort: If the file does not exist or is not a supported image type, abort the command.
    """
    # get the file path
    file: Path = Path(file_path)

    # check if the file exists
    if not file.is_file():
        print(f"[bold red]Error:[/bold red] The file `{file.name}` does not exist.")
        raise typer.Abort()

    # check if the file is a supported image type
    if not (file.suffix in SUPPORTED_IMAGES_EXTENSIONS):
        print(
            f"[bold red]Error:[/bold red] The file `{file_path}` is not a supported image type."
        )
        raise typer.Abort()

    print(f"Uploading [blue italic]{file.name}[/blue italic] to GitHhub")

    # read the file content and encode it to base64
    with open(str(file), "rb") as image_file:
        content = base64.b64encode(image_file.read()).decode("utf-8")

    # build the DTO
    upload_file_dto = controller.UploadMediaInputDTO(
        media_title=file.name, media_data=content, media_description=description
    )

    # upload the file
    try:
        controller.upload_media(upload_file_dto)
    except UploadMediaError as e:
        print(
            f"[bold red]Error:[/bold red] Failed to upload file `{file.name}` to GitHub. {e}"
        )
        raise typer.Abort()
    except DuplicateMediaError as e:
        print(
            f"[bold red]Error:[/bold red] File `{file.name}` already exists in the repository. {e}"
        )
        raise typer.Abort()
    except Exception as e:
        print(f"[bold red]Error:[/bold red] An error occurred. {e}")
        raise typer.Abort()

    print(
        f"[green bold]File {file.name} was successfully uploaded to GitHub.[/green bold]"
    )


@app.command()
def upload_directory(directory_path: str) -> None:

    # convert the directory path to a Path object
    directory = Path(directory_path)

    # check if the directory exists
    if not directory.is_dir():
        print(
            f"[bold red]Error:[/bold red] The directory `{directory.name}` does not exist."
        )
        raise typer.Abort()

    # get the elements in the directory
    elements: Set[Path] = set(directory.iterdir())

    # check if the directory is empty
    if not elements:
        print(f"[bold red]Error:[/bold red] The directory `{directory.name}` is empty.")
        raise typer.Abort()

    # filter the elements to only include supported image types
    filtered_elements: Set[Path] = {
        e for e in elements if e.suffix in SUPPORTED_IMAGES_EXTENSIONS
    }

    # check if there are unsupported image types
    if filtered_elements != elements:
        print(
            f"[bold yellow]Warning:[/bold yellow] Some files in the directory `{directory.name}` "
            f"are not supported image types ({", ".join(SUPPORTED_IMAGES_EXTENSIONS)}): "
            f"\n {"\n".join([str(e) for e in elements - filtered_elements])}"
        )
        typer.confirm(
            text="Do you want to continue uploading the supported image types?",
            default=False,
            abort=True,
            show_default=True,
        )

    print(f"Uploading [blue italic]{directory.name}[/blue italic] directory to GitHub")

    # iterate over the filtered elements and upload them
    for element in filtered_elements:
        print(f"Uploading [blue italic]{element.name}[/blue italic] to GitHub")
        dto = controller.UploadMediaInputDTO(
            media_title=element.name,
            media_data=base64.b64encode(element.read_bytes()).decode("utf-8"),
        )
        controller.upload_media(dto)

    print(
        f"[green bold]Directory {directory.name} was successfully uploaded to GitHub.[/green bold]"
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
