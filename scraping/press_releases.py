import time
from bs4 import BeautifulSoup
import httpx
import pandas as pd


def get_press_releases():
    URL = 'http://www.cbr.ru/Crosscut/NewsList/LoadMore/84035?intOffset=0&extOffset='
    offset = 0
    data = []

    while True:
        page = httpx.get(URL + str(offset))
        if len(page.text.strip()) == 0:
            break

        tree = BeautifulSoup(page.text, "html.parser")
        releases = tree.select(".previews_day")
        for item in releases:
            date = item.select_one(".previews_day-date")
            links = item.select("a")

            for link in links:
                data_item = []
                data_item.append(date.text)
                data_item.append("http://www.cbr.ru" + link["href"])
                data_item.append(link.text.strip())
                data.append(data_item)

        offset += 10
        time.sleep(1)

    for i, (_, link, _) in enumerate(data):
        response = httpx.get(link)
        tree = BeautifulSoup(response.text, 'html.parser')
        release = tree.find_all('div', {'class': 'landing-text'})[0]
        data[i].append(release.text.strip())
        time.sleep(1)

    df = pd.DataFrame(data, columns=['date', 'link', 'title', 'release'])
    df.to_csv('../data/raw-cbr-press-releases.csv', index=False)


if __name__ == "__main__":
    get_press_releases()
