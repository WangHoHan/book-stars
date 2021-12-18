from bs4 import BeautifulSoup
import csv
import requests
import re

lubimyczytac = f"https://lubimyczytac.pl/katalog?page=1&listId=booksFilteredList&onlyPublished=1&publishedYear%5B0%5D=1200&publishedYear%5B1%5D=2021&catalogSortBy=published-desc&paginatorType=Standard"
page = requests.get(lubimyczytac).text
doc = BeautifulSoup(page, "html.parser")
no_pages = 0
no_pages_match = re.search(r"\d+", str(doc.findAll(class_="page-link stdPaginator btn")[-1]))
if no_pages_match:
    no_pages = int(no_pages_match.group())
with open("book_stars.csv", "w", newline='', encoding='utf-8') as book_stars:
    writer = csv.writer(book_stars)
    for page in range(1, no_pages + 1):
        # print("page: ", page, "/", no_pages, sep="")
        lubimyczytac = f"https://lubimyczytac.pl/katalog?page={page}&listId=booksFilteredList&onlyPublished=1&publishedYear%5B0%5D=1200&publishedYear%5B1%5D=2021&catalogSortBy=published-desc&paginatorType=Standard"
        page = requests.get(lubimyczytac).text
        doc = BeautifulSoup(page, "html.parser")
        books_match = re.findall(r'href=\"(.+)\">', str(doc.findAll(class_="authorAllBooks__singleTextTitle float-left")))
        for book in books_match:
            # print("book: ", book.rsplit('/', 1)[-1], sep="")
            lubimyczytac = f"https://lubimyczytac.pl" + book
            page = requests.get(lubimyczytac).text
            doc = BeautifulSoup(page, "html.parser")
            posts = doc.findAll(class_="comment-cloud")
            for post in posts:
                star = re.search(r'<span class="icon icon-icon-star-full red"></span>\n<span class="big-number">\n(\d\d?)', str(post), flags=re.DOTALL)
                if star:
                    opinion = re.findall(r'<p class="p-expanded js-expanded mb-0" style="display:none;">(.*)<\/p>.*<p class="p-collapsed js-collapsed mb-0">.*', str(post), flags=re.DOTALL)
                    if opinion:
                        opinion[0] = opinion[0].replace("\n", " ").replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("</br>", "").replace("<br/>", "")
                        opinion[0] = re.sub(" +", " ", opinion[0])
                        # print("star: ", star.group(1), sep="", end=", ")
                        # print("opinion: ", opinion[0], sep="")
                        try:
                            writer.writerow([star.group(1), opinion[0]])
                        except:
                            pass
