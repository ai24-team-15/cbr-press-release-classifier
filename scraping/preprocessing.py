import pandas as pd
import re


def calc_target(row):
    if 'сохранить' in row['title'] or 'сохранил' in row['title']:
        return 0
    elif 'повысить' in row['title']:
        return 1
    elif 'снизить' in row['title']:
        return -1
    else:
        end = 150
        
        if ('О ключевой ставке Банка России' in row['title'] 
            or 'О процентных ставках по операциям Банка России' in row['title']):

            if 'сохранить' in row['release'][:end] or 'оставить' in row['release'][:end]:
                return 0
            elif 'повысить' in row['release'][:end]:
                return 1
            elif 'снизить' in row['release'][:end]:
                return -1


def get_rate(row):
    m = re.search(r'до\s+(\d+,?\d*)%', row.release)
    if m is None or m.start(1) > 200:
        m = re.search(r'(\d+,?\d*)%', row.release)
    return float(m.group(1).replace(',', '.'))


df = pd.read_csv('../data/raw-cbr-press-releases.csv')
df['target'] = df.apply(calc_target, axis=1)

df.dropna(subset=['target'], inplace=True)
df.reset_index(drop=True, inplace=True)

df['interest_rate'] = df.apply(get_rate, axis=1)

df.target = df.target.shift(1)
df.interest_rate = df.interest_rate.shift(1)

df.to_csv('../data/cbr-press-releases.csv', index=False)


