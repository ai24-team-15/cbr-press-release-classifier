import pandas as pd
import numpy as np


def make_preprocessing():
    df_releases = pd.read_csv('../data/raw-cbr-press-releases.csv')
    df_releases['date'] = df_releases['date'].str.replace(' г.', '')
    df_releases['date'] = df_releases['date'].str.replace(' января ', '.01.')
    df_releases['date'] = df_releases['date'].str.replace(' февраля ', '.02.')
    df_releases['date'] = df_releases['date'].str.replace(' марта ', '.03.')
    df_releases['date'] = df_releases['date'].str.replace(' апреля ', '.04.')
    df_releases['date'] = df_releases['date'].str.replace(' мая ', '.05.')
    df_releases['date'] = df_releases['date'].str.replace(' июня ', '.06.')
    df_releases['date'] = df_releases['date'].str.replace(' июля ', '.07.')
    df_releases['date'] = df_releases['date'].str.replace(' августа ', '.08.')
    df_releases['date'] = df_releases['date'].str.replace(' сентября ', '.09.')
    df_releases['date'] = df_releases['date'].str.replace(' октября ', '.10.')
    df_releases['date'] = df_releases['date'].str.replace(' ноября ', '.11.')
    df_releases['date'] = df_releases['date'].str.replace(' декабря ', '.12.')
    df_releases['date'] = pd.to_datetime(df_releases['date'], dayfirst=True)

    df_key_rates = pd.read_csv('../data/key-rates-cbr.csv')
    df_key_rates['date'] = pd.to_datetime(df_key_rates['date'], dayfirst=True)

    df_all = df_releases.set_index('date').join(
        df_key_rates.set_index('date'), how='outer')

    df_all['rate_before'] = df_all['rate'].shift(1)
    last_rate = df_all.iloc[-1]['rate']
    df_all = df_all[~df_all['release'].isna()]

    df_all['rate'] = df_all['rate_before'].shift(-2)
    df_all.at[df_all.index[-2], 'rate'] = last_rate
    df_all = df_all.drop(columns=['rate_before'])

    df_all = df_all.reset_index()
    df_all['days_between'] = (df_all['date'] - df_all['date'].shift(1)).dt.days
    df_all['days_between'] = df_all['days_between'].shift(-1)

    df_all['target_categorial'] = np.sign(df_all['rate'] -
                                          df_all['rate'].shift(1))
    df_all['target_absolute'] = df_all['rate'] - df_all['rate'].shift(1)
    df_all['target_relative'] = df_all['rate'] / df_all['rate'].shift(1)

    df_all.at[df_all.index[0], 'target_categorial'] = 0
    df_all.at[df_all.index[0], 'target_absolute'] = 0
    df_all.at[df_all.index[0], 'target_relative'] = 1

    df_all.to_csv('../data/cbr-press-releases.csv', index=False)


if __name__ == "__main__":
    make_preprocessing()