import datetime as dt
from pathlib import Path

from PIL import ExifTags, Image, UnidentifiedImageError

EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"
OUT_DATE_FORMAT = "%Y%m%d-%H%M%S"


def rename_images(path: str, suffix: str | None = None, dry_run: bool = True):
    imgDir = Path(path)
    changes = plan(imgDir, suffix)
    if dry_run:
        simulate(changes)
    else:
        apply(changes)


def plan(imgDir: Path, suffix: str | None):
    changes: dict[str, str] = {}

    for fp in imgDir.iterdir():
        try:
            with Image.open(fp) as img:
                dtRaw = img.getexif().get_ifd(ExifTags.IFD.Exif)[
                    ExifTags.Base.DateTimeOriginal
                ]
            dtParsed = dt.datetime.strptime(dtRaw, EXIF_DATE_FORMAT)
            sffx = "-" + suffix if suffix else ""
            name = dtParsed.strftime(OUT_DATE_FORMAT) + sffx
            # Avoid name collisions causing files to be overwritten
            newPath = fp.with_stem(name)
            i = 1
            while str(newPath) in changes:
                newPath = fp.with_stem(f"{name}-{i}")
                i += 1
            changes[str(newPath)] = str(fp)

        except UnidentifiedImageError, IsADirectoryError, PermissionError, KeyError:
            changes[str(fp)] = str(fp)
            continue

    return changes


def simulate(changes: dict[str, str]):
    renamed = 0
    for new, old in changes.items():
        if new == old:
            print("Skipping " + old)
        else:
            print(f"{old} -> {new}")
            renamed += 1
    print(f"{len(changes)} files found, {renamed} files renamed.")


def apply(changes: dict[str, str]):
    renamed = 0
    for new, old in changes.items():
        if new == old:
            continue
        op = Path(old)
        np = Path(new)
        if np.exists():
            raise FileExistsError(
                f"File {np} already exists. Aborting to avoid overwriting."
            )
        op.rename(np)
        renamed += 1
    print(f"{len(changes)} files found, {renamed} files renamed.")
