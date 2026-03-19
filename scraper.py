import requests
from bs4 import BeautifulSoup
import pandas as pd

current_pages = 1
max_pages = 50
data = []

while current_pages <= max_pages:
    print(f"Currently Scraping Page: {current_pages}")
    url = f"https://books.toscrape.com/catalogue/page-{current_pages}.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    if "404" in soup.title.text or "page not found" in soup.title.text:
        print("reached the end of website!")
        break
    else:
        all_books = soup.find_all("li" ,class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for book in all_books:
            item ={}
            item["Title"] = book.find('img').attrs['alt']
            item["Link"] = book.find('a').attrs['href']
            item["price"] = book.find('p', class_ ="price_color").text
            item["stock"] = book.find('p', class_ ="instock availability").text.strip()
            data.append(item)

    current_pages+=1

df = pd.DataFrame(data)
df.to_csv("books_data.csv", index=False)
print(df.head())