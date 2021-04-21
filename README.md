# Hindawi downloader

Download all books from Hindawi organization's website in PDF format.

## Pre-requisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/)

## Installation

- Open terminal inside the project's folder
- `$ poetry install`

## Usage

- `$ python download.py all-books` download all the books (2147) sequentially. Beware, a lot of Gigabytes :))
- `$ python download.py starting-from <line_number>` download all books starting from line number inside the [books_data.csv](books_data.csv) file, useful when the above command is interrupted
- `$ python download.py book <book_id>` download a specific book using its id

## Notes

- You'll find the downloaded books inside the [downloaded_books](downloaded_books) folder (will be automatically created when you run the command)
- [get_books_data.py](get_books_data.py) is used to get the all books data upfront in form of (id, title, pdf_url)
- [books_data.csv](books_data.csv) is already downloaded for you! You don't need to use the [get_books_data.py](get_books_data.py) script unless you want to remove the [books_data.csv](books_data.csv) file and re-generate it again.


**Thank you** :smile:
