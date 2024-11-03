import pandas as pd
import numpy as np


def make_preprocessing():
    df_releases = pd.read_csv("../data/raw-cbr-press-releases.csv")
    df_releases["date"] = df_releases["date"].str.replace(" г.", "")
    df_releases["date"] = df_releases["date"].str.replace(" января ", ".01.")
    df_releases["date"] = df_releases["date"].str.replace(" февраля ", ".02.")
    df_releases["date"] = df_releases["date"].str.replace(" марта ", ".03.")
    df_releases["date"] = df_releases["date"].str.replace(" апреля ", ".04.")
    df_releases["date"] = df_releases["date"].str.replace(" мая ", ".05.")
    df_releases["date"] = df_releases["date"].str.replace(" июня ", ".06.")
    df_releases["date"] = df_releases["date"].str.replace(" июля ", ".07.")
    df_releases["date"] = df_releases["date"].str.replace(" августа ", ".08.")
    df_releases["date"] = df_releases["date"].str.replace(" сентября ", ".09.")
    df_releases["date"] = df_releases["date"].str.replace(" октября ", ".10.")
    df_releases["date"] = df_releases["date"].str.replace(" ноября ", ".11.")
    df_releases["date"] = df_releases["date"].str.replace(" декабря ", ".12.")
    df_releases["date"] = pd.to_datetime(df_releases["date"], dayfirst=True)
    df_releases = df_releases[
        (df_releases["link"] != "http://www.cbr.ru/press/pr/?file=130913_1350427l.htm")
        & (df_releases["link"] != "http://www.cbr.ru/press/pr/?file=06052015_163917if2015-05-06T16_30_05.htm")
        & (df_releases["link"] != "http://www.cbr.ru/press/pr/?file=11092015_160009if2015-09-11T15_43_15.htm")
        & (df_releases["link"] != "http://www.cbr.ru/press/pr/?file=29122015_113403if2015-12-29T10_44_49.htm")
    ]

    df_releases["date_my"] = df_releases["date"].dt.strftime("%m.%Y")
    df_key_rates = pd.read_csv("../data/key-rates-cbr.csv")
    df_key_rates["date"] = pd.to_datetime(df_key_rates["date"], dayfirst=True)

    df_cur_usd = pd.read_csv("../data/cur-usd-cbr.csv")
    df_cur_usd["date"] = pd.to_datetime(df_cur_usd["date"], dayfirst=True)

    df_inf = pd.read_csv(
        "../data/inflation-cbr.csv",
        dtype={"date_inflation": "str", "inflation": "float"},
    )

    df_releases = pd.merge(df_releases, df_inf, left_on="date_my", right_on="date_inflation", how="left")
    df_releases = df_releases.drop(["date_my", "date_inflation"], axis=1)

    df_all = (
        df_releases.set_index("date")
        .join(df_key_rates.set_index("date"), how="outer")
        .join(df_cur_usd.set_index("date"), how="left")
    )

    df_all["rate_before"] = df_all["rate"].shift(1)
    last_rate = None
    if pd.isna(df_all.iloc[-1]["release"]):
        last_rate = df_all.iloc[-1]["rate"]
    df_all = df_all[~df_all["release"].isna()]

    df_all["usd"] = df_all["usd"].bfill()

    df_all["rate"] = df_all["rate_before"].shift(-2)
    df_all.at[df_all.index[-2], "rate"] = last_rate
    df_all = df_all.drop(columns=["rate_before"])

    df_all = df_all.reset_index()
    df_all["days_between"] = (df_all["date"] - df_all["date"].shift(1)).dt.days
    df_all["days_between"] = df_all["days_between"].shift(-1)

    df_all["usd_cur_change_relative"] = df_all["usd"] / df_all["usd"].shift(1)
    df_all["usd_cur_change_relative"] = df_all["usd_cur_change_relative"].shift(-1)
    df_all["usd"] = df_all["usd"].shift(-1)
    df_all["inflation"] = df_all["inflation"].shift(-1)

    df_all["target_categorial"] = np.sign(df_all["rate"] - df_all["rate"].shift(1))
    df_all["target_absolute"] = df_all["rate"] - df_all["rate"].shift(1)
    df_all["target_relative"] = df_all["rate"] / df_all["rate"].shift(1)

    df_all.at[df_all.index[0], "target_categorial"] = 0
    df_all.at[df_all.index[0], "target_absolute"] = 0
    df_all.at[df_all.index[0], "target_relative"] = 1

    df_all = df_all[
        [
            "date",
            "link",
            "title",
            "release",
            "days_between",
            "rate",
            "inflation",
            "usd",
            "usd_cur_change_relative",
            "target_categorial",
            "target_absolute",
            "target_relative",
        ]
    ]

    df_all.to_csv("../data/cbr-press-releases.csv", index=False)


if __name__ == "__main__":
    make_preprocessing()
