import pandas as pd


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


df = pd.read_csv('../data/raw-cbr-press-releases.csv')
df['target'] = df.apply(calc_target, axis=1)

df.dropna(subset=['target'], inplace=True)
df.reset_index(drop=True, inplace=True)

df['interest_rate'] = df.release.str.extract(r'(\d*\d,*\d*\d*%)')

df.target = df.target.shift(1)
df.interest_rate = df.interest_rate.shift(1)

df.to_csv('../data/cbr-press-releases.csv', index=False)


