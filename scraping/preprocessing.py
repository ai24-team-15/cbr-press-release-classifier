import locale
from datetime import datetime

import pandas as pd
import numpy as np

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

RELEASES_TO_DELETE = {
    "http://www.cbr.ru/press/pr/?file=130913_1350427l.htm",
    "http://www.cbr.ru/press/pr/?file=06052015_163917if2015-05-06T16_30_05.htm",
    "http://www.cbr.ru/press/pr/?file=11092015_160009if2015-09-11T15_43_15.htm",
    "http://www.cbr.ru/press/pr/?file=29122015_113403if2015-12-29T10_44_49.htm"
}


def make_preprocessing():
    df_releases = pd.read_csv("../data/raw-cbr-press-releases.csv")

    def calc_date(value):
        day, month, year, _ = value.split()
        month = month[:3] # .replace('мая', 'май')
        return datetime.strptime(' '.join([day, month, year]), '%d %b %Y')
    
    df_releases.date = df_releases.date.map(calc_date)

    df_releases = df_releases.query("link not in @RELEASES_TO_DELETE")

    df_releases["month"] = df_releases["date"].dt.strftime("%m.%Y")
    df_key_rates = pd.read_csv("../data/key-rates-cbr.csv", parse_dates=['date'], dayfirst=True)

    max_date = df_key_rates["date"].max()
    df_releases = df_releases.query("date < @max_date")

    df_key_rates["date"] = pd.to_datetime(df_key_rates["date"], dayfirst=True)

    df_cur_usd = pd.read_csv("../data/cur-usd-cbr.csv")
    df_cur_usd["date"] = pd.to_datetime(df_cur_usd["date"], dayfirst=True)

    df_inf = pd.read_csv(
        "../data/inflation-cbr.csv",
        dtype={"date_inflation": "str", "inflation": "float"},
    )

    df_inf.inflation = df_inf.inflation.shift(-1)

    df_releases = pd.merge(
        df_releases, df_inf, 
        left_on="month", 
        right_on="date_inflation", 
        how="left"
        )
    df_releases = df_releases.drop(["month", "date_inflation"], axis=1)

    df_all = (
        df_releases.set_index("date")
        .join(df_key_rates.set_index("date"), how="outer")
        .join(df_cur_usd.set_index("date"), how="left")
    )
    df_all["usd"] = df_all["usd"].bfill()

    df_all['rate'] = df_all.rate.shift(-2)
    df_all.dropna(subset=["release"], inplace=True)
    df_all['rate'] = df_all['rate'].shift(-1)

    df_all["usd_cur_change_relative"] = df_all["usd"] / df_all["usd"].shift(1)

    df_all["target_categorial"] = np.sign(df_all["rate"] - df_all["rate"].shift(1))
    df_all["target_absolute"] = df_all["rate"] - df_all["rate"].shift(1)
    df_all["target_relative"] = df_all["rate"] / df_all["rate"].shift(1)

    df_all.at[df_all.index[0], "target_categorial"] = 0 
    df_all.at[df_all.index[0], "target_absolute"] = 0
    df_all.at[df_all.index[0], "target_relative"] = 1
    df_all.at[df_all.index[0], "usd_cur_change_relative"] = df_all.at[df_all.index[0], "usd"] /  32.8606
    df_all.at[df_all.index[0], "inflation"] = 6.51

    df_all.to_csv("../data/cbr-press-releases.csv", index=True)


if __name__ == "__main__":
    make_preprocessing()
