from pathlib import Path
from typing import Annotated

import typer

from .core import rename_images

app = typer.Typer()


@app.command()
def cli(
    path: Annotated[str, typer.Argument()],
    suffix: str | None = None,
    dry_run: bool = True,
):
    rename_images(path, suffix, dry_run)
