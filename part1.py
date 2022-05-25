from bs4 import BeautifulSoup
import requests


session = requests.session()

def getSoupObject(page_url):
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 '
                      'Safari / 537.36',
        'Accept-Language': 'en-US, en;q=0.5'})
    webpage = session.get(page_url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    return soup

def catchException(data, tag, class_name):
    try:
        if tag == 'a':
            file.write(f"https://amazon.in{data.find(tag, class_name)['href']},")
            return
        file.write(f"{data.find(tag, class_name).text}".replace(",", "") + ",")
    except AttributeError:
        file.write("Cannot Scrape,")

def getSeparatedData(soup):
    products_data = soup.find_all("div", {"class": "s-card-container s-overflow-hidden aok-relative "
                                                   "s-include-content-margin s-latency-cf-section s-card-border"})
    for data in products_data:
        catchException(data, "a", {
            "class": "a-link-normal " "s-underline-text " "s-underline-link" "-text " "s-link-style " "a-text-normal"})
        catchException(data, "span", {"class": "a-size-medium a-color-base a-text-normal"})
        catchException(data, "span", {"class": "a-price-whole"})
        catchException(data, "span", {"class": "a-icon-alt"})
        catchException(data, "span", {"class": "a-size-base s-underline-text"})
        file.write("\n")

def getNextPage(soup):
    return "https://amazon.in" + soup.find("a", {'class': 's-pagination-item s-pagination-button'})["href"]

def main(url):
    for _ in range(19):
        soupObject = getSoupObject(url)
        getSeparatedData(soupObject)
        url = getNextPage(soupObject)


if __name__ == '__main__':
    url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
    with open("part1.csv", "a") as file:
        main(url)
