import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def encoding_mapping(df):
    mapped_df = df
    ordinal_mapping = {'free': 0, '<$15': 1, '$15-25': 2, '$25-50': 3, '$59.99': 4, '>$60': 5}
    mapped_df['Price'] = mapped_df['Price'].astype(str).map(ordinal_mapping)
    genre_mapping = {'AA': 11, 'RP': 12, 'ST': 13, 'SM': 14, 'SR': 15, 'VN': 16, 'PG': 17}
    mapped_df['Genre'] = mapped_df['Genre'].astype(str).map(genre_mapping)
    theme_mapping = {'AN': 0, 'HR': 1, 'MY': 2, 'SF': 3, 'FN': 4, 'PA': 5, 'HS': 6, 'MD': 7, 'WA': 8, 'SH': 9, 'PG': 10}
    mapped_df['Theme'] = mapped_df['Theme'].astype(str).map(theme_mapping)
    return mapped_df

def all_data():
    ImportData = pd.read_csv("game_data_no_outliers.csv")
    GameData = encoding_mapping(ImportData)
    y = GameData['Copies_per_year']
    X = GameData.drop('Copies_per_year', axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scale_column = 'Copies_per_year'
    scaler = StandardScaler()
    y_train = y_train.to_frame()
    y_test = y_test.to_frame()
    y_train[[scale_column]] = scaler.fit_transform(y_train[[scale_column]])
    y_test[[scale_column]] = scaler.transform(y_test[[scale_column]])

    rfm = RandomForestRegressor(random_state=42, n_estimators=1000)
    rfm.fit(X_train, y_train.values.ravel())
    y_pred = rfm.predict(X_test)

    return GameData, rfm, y_test, y_pred
