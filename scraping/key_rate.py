import httpx
from bs4 import BeautifulSoup
import pandas as pd


def get_key_rate():
    base_url = "https://cbr.ru/hd_base/KeyRate"
    response = httpx.get(base_url)
    scripts = BeautifulSoup(response.text, "html.parser").find_all("script")
    script_str = scripts[22].get_text()
    dates_str = script_str.split(',"categories":["')[1].split("]")[0]
    values_str = script_str.split(',"data":[')[1].split("]")[0]

    dates_array = [s.strip('"') for s in dates_str.split(",")]
    values_array = [float(s) for s in values_str.split(",")]

    dict = {"date": dates_array, "rate": values_array}
    df = pd.DataFrame(dict)
    df.to_csv("../data/key-rates-cbr.csv", index=False)


if __name__ == "__main__":
    get_key_rate()
