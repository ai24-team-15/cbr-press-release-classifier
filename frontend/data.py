import pandas as pd
from utils import preprocessing_release

DATA = pd.read_csv('../data/cbr-press-releases.csv')

DATA['target_categorial_name'] = DATA.target_categorial.map(
        {
            -1: 'Снижение ставки', 
            1: 'Повышение ставки', 
            0: 'Сохранение ставки'
        }
    )

DATA['corpus'] = DATA.release.apply(preprocessing_release)
