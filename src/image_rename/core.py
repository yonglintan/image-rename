import datetime as dt
from pathlib import Path

from PIL import ExifTags, Image, UnidentifiedImageError

EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"
OUT_DATE_FORMAT = "%Y%m%d-%H%M%S"


def rename_images(path, suffix=None):
    imgDir = Path(path)

    for fp in imgDir.iterdir():
        try:
            with Image.open(fp) as img:
                dtRaw = img.getexif().get_ifd(ExifTags.IFD.Exif)[
                    ExifTags.Base.DateTimeOriginal
                ]
            dtParsed = dt.datetime.strptime(dtRaw, EXIF_DATE_FORMAT)
            sffx = "-" + suffix if suffix else ""
            basename = dtParsed.strftime(OUT_DATE_FORMAT) + sffx
            # Avoid name collisions causing files to be overwritten
            newPath = fp.with_stem(basename)
            i = 1
            while newPath.exists():
                newPath = fp.with_stem(basename + "-" + str(i))
                i += 1
            fp.rename(newPath)

        except UnidentifiedImageError:
            continue
