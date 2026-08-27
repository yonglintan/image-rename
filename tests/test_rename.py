import datetime as dt
from pathlib import Path

import pytest
from PIL import ExifTags, Image, UnidentifiedImageError

from image_rename.core import rename_images

EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"


@pytest.fixture
def img_dir():
    N = 100
    N_DUPES = 1

    startdate = dt.datetime(2011, 11, 11)
    tendays = dt.timedelta(days=10)

    # Create directory of images with DateTimeOriginal EXIF data
    img_dir = Path("temp")
    img_dir.mkdir(exist_ok=True)

    for i in range(N):
        img = Image.new("1", (100, 100))
        imgDate = i * tendays + startdate if i < N - N_DUPES else startdate
        exif = img.getexif()
        exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
        exif_ifd[ExifTags.Base.DateTimeOriginal] = imgDate.strftime(EXIF_DATE_FORMAT)
        img.save(img_dir / f"test{i}.jpeg", exif=exif.tobytes())

    img_dir.joinpath("not-an-image.txt").touch()
    img_dir.joinpath("subdir").mkdir(exist_ok=True)

    yield img_dir

    # Cleanup
    for file in img_dir.iterdir():
        if file.is_dir():
            file.rmdir()
        else:
            file.unlink(missing_ok=True)
    img_dir.rmdir()


def test_rename(img_dir):
    # Count items in directory
    count = 0
    for i in img_dir.iterdir():
        count += 1

    # Run rename function
    rename_images(img_dir)

    # Check that the name of every image in directory starts with date that corresponds to EXIF data
    for file in img_dir.iterdir():
        count -= 1
        try:
            with Image.open(file) as im:
                dtRaw = im.getexif().get_ifd(ExifTags.IFD.Exif)[
                    ExifTags.Base.DateTimeOriginal
                ]
                expected = dt.datetime.strptime(dtRaw, EXIF_DATE_FORMAT).strftime(
                    "%Y%m%d-%H%M%S"
                )
                assert file.name.startswith(expected)
        except UnidentifiedImageError:
            continue

    # Check that the number of items in the directory is the same as before
    assert count == 0
