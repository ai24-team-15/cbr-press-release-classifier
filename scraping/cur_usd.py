import httpx
from bs4 import BeautifulSoup
import pandas as pd


def get_cur_usd():
    base_url = (
        "https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&"
        "UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From=01.09.2013"
    )
    response = httpx.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find("table", attrs={"class": "data"}).find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        cols = [c.text.strip() for c in cols]
        if len(cols) == 3:
            data.append([cols[0], float(cols[2].replace(",", "."))])

    df = pd.DataFrame(data, columns=["date", "usd"])
    df.to_csv("../data/cur-usd-cbr.csv", index=False)


if __name__ == "__main__":
    get_cur_usd()
