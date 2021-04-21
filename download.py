import csv
import logging
import unicodedata
import re
import requests
import typer
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Path("downloaded_books").mkdir(parents=True, exist_ok=True)
app = typer.Typer()


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def download_file(url, file_name):
    """Download a file using requests"""

    local_filename = f"{slugify(file_name.strip())}.pdf"

    # skip pre-downloaded files
    if Path(local_filename).is_file():
        return

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f"downloaded_books/{local_filename}", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


@app.command()
def all_books():
    """Download all available books"""

    with open("books_data.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 1
        for row in csv_reader:
            if line_count == 1:
                logging.info("passing header")
            else:
                logging.info(
                    f"Downloading #{line_count} of 2147, id: {row[0]}, title: {row[1]}"
                )
                download_file(row[2], row[1])
            line_count += 1

        logging.info(f"Downloaded {line_count} books.")


@app.command()
def starting_from(line_number: int):
    """Download books starting from a line number specified from the books_data.csv file"""

    with open("books_data.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 1
        for row in csv_reader:
            if line_count < line_number:
                line_count += 1
                continue
            else:
                logging.info(
                    f"Downloading #{line_count}, id: {row[0]}, title: {row[1]}"
                )
                download_file(row[2], row[1])
                line_count += 1

        logging.info(f"Downloaded {line_count - line_number} books.")


@app.command()
def book(book_id: str):
    """Download as single book by id"""
    with open("books_data.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for line_count, row in enumerate(csv_reader, start=1):
            if line_count == 1:
                logging.info("passing header")
            else:
                if row[0] == book_id:
                    logging.info(
                        f"Downloading #{line_count}, id: {row[0]}, title: {row[1]}"
                    )
                    download_file(row[2], row[1])
                    logger.info("Done.")


if __name__ == "__main__":
    app()