import csv
import requests
import logging

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ["id", "name", "pdf_url"]
all_books = []

pages = [f"https://www.hindawi.org/books/{n}/" for n in range(1, 216)]

for page in pages:
    logger.info(f"Entering {page}")

    resp = requests.get(page)
    soup = BeautifulSoup(resp.text, "html.parser")
    page_books = soup.find_all(class_="book")

    for book in page_books:
        details = book.find(class_="details")
        id = details.h2.a["href"].split("/")[2]
        name = details.h2.a.text.strip()
        pdf_url = f"https://www.hindawi.org/books/{id}.pdf"

        all_books.append([id, name, pdf_url])
        logger.info(f"{id}, {name}, {pdf_url}")


with open("all_books.csv", mode="w") as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["id", "name", "pdf_url"])
    for book in all_books:
        writer.writerow([book[0], book[1], book[2]])
