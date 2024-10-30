import httpx
from bs4 import BeautifulSoup
import pandas as pd


def get_inflation():
    base_url = 'https://www.cbr.ru/hd_base/infl/?UniDbQuery.Posted=True&UniDbQuery.From=17.09.2013'
    response = httpx.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find('table', attrs={'class': 'data'}).find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [c.text.strip() for c in cols]
        if len(cols) == 4:
            data.append([cols[0], float(cols[2].replace(',', '.'))])

    df = pd.DataFrame(data, columns=['date_inflation', 'inflation'])
    df.to_csv('../data/inflation-cbr.csv', index=False)


if __name__ == "__main__":
    get_inflation()
