import csv
import logging
import requests
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Path("downloaded_books").mkdir(parents=True, exist_ok=True)


def download_file(url, file_name):
    local_filename = f"{file_name}.pdf"

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f"downloaded_books/{local_filename}", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return local_filename


with open("all_books.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            logging.info("passing header")
        else:
            logging.info(f"Downloading: {row[0]}")
            download_file(row[2], row[1])

        line_count += 1

    print(f"Downloaded {line_count} books.")
