import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import explained_variance_score, mean_squared_error, r2_score

from model import all_data


def initialize_model():
    global df, model, test, predict, indv
    df, model, test, predict = all_data()
    indv = df.drop('Copies_per_year', axis=1)


def get_feature_import():
    import_sum, value = 0, 0
    sales_impact = []
    column_indices = [indv.columns.get_loc(col) for col in indv.columns]
    for header in column_indices:
        value = model.feature_importances_[header]
        import_sum = import_sum + value
    for header in range(0, 3):
        import_value = model.feature_importances_[header]
        title = indv.columns[header]
        import_percent = (import_value / import_sum) * 100
        sales_impact.append((title, import_percent))
    return sales_impact


def get_best_features():
    best_features = []
    for header in range(3, 30):
        if model.feature_importances_[header] > 0.03:
            best_features.append(indv.columns[header])
    return best_features


def get_worst_features():
    worst_features = []
    for header in range(3, 30):
        if model.feature_importances_[header] < 0.01:
            worst_features.append(indv.columns[header])
    return worst_features


def get_mse():
    mse = mean_squared_error(test, predict)
    return mse


def get_explained_var():
    explained_var = explained_variance_score(test, predict)
    return explained_var


def get_r2():
    r2 = r2_score(test, predict)
    return r2


def get_residuals():
    test_array = test.values.flatten()
    residuals = (test_array - predict)
    return residuals


def get_y_pred():
    return predict


def get_variance():
    low_val = 0
    high_val = 0
    for v in test.values:
        if float(v) < low_val:
            low_val = float(v)
        if float(v) > high_val:
            high_val = float(v)
    variance = high_val - low_val
    return variance


def model_by_genre(selected_genre):
    num_genre = all_mapping(selected_genre)
    genre_subset = df[df['Genre'] == num_genre]
    grouped_df = pd.DataFrame(columns=['Theme', 'Actual_Sales', 'Predicted_Sales'])

    X = genre_subset.drop('Copies_per_year', axis=1)
    y = genre_subset['Copies_per_year']
    mini_model = RandomForestRegressor()
    mini_model.fit(X, y)

    for theme in range(10):
        theme_data = genre_subset[genre_subset['Theme'] == theme]
        if not theme_data.empty:
            avg_actual_sales = theme_data['Copies_per_year'].mean()
            avg_predicted_sales = mini_model.predict(theme_data.drop('Copies_per_year', axis=1)).mean()
        else:
            avg_actual_sales = 0
            avg_predicted_sales = 0

        grouped_df = pd.concat([grouped_df, pd.DataFrame({'Theme': [theme], 'Actual_Sales': [avg_actual_sales],
                                                          'Predicted_Sales': [avg_predicted_sales]})])

    return grouped_df.reset_index(drop=True)


def model_by_theme(selected_theme):
    num_theme = all_mapping(selected_theme)
    theme_subset = df[df['Theme'] == num_theme]
    grouped_df = pd.DataFrame(columns=['Genre', 'Actual_Sales', 'Predicted_Sales'])

    X = theme_subset.drop('Copies_per_year', axis=1)
    y = theme_subset['Copies_per_year']
    mini_model = RandomForestRegressor()
    mini_model.fit(X, y)

    for genre in range(11, 17):
        genre_data = theme_subset[theme_subset['Genre'] == genre]
        if not genre_data.empty:
            avg_actual_sales = genre_data['Copies_per_year'].mean()
            avg_predicted_sales = mini_model.predict(genre_data.drop('Copies_per_year', axis=1)).mean()
        else:
            avg_actual_sales = 0
            avg_predicted_sales = 0

        grouped_df = pd.concat([grouped_df, pd.DataFrame({'Genre': [genre], 'Actual_Sales': [avg_actual_sales],
                                                          'Predicted_Sales': [avg_predicted_sales]})])

    return grouped_df.reset_index(drop=True)


def all_mapping(key):

    forward_map = {"Anime": 0, "Horror": 1, "Mystery": 2, "Science-fiction": 3, "Fantasy": 4, "Post-apocalyptic": 5,
                   "History": 6, "Modern": 7, "War": 8, "Superhero": 9, "Action-Adventure": 11, "Party Games": 17,
                   "Role-Playing": 12, "Strategy": 13, "Simulation": 14, "Sports and Racing": 15, "Visual Novels": 16}

    backward_map = {11: "Action-Adventure", 12: "Role-Playing", 13: "Strategy", 14: "Simulation", 15: "Sports and Racing",
                    16: "Visual Novels", 17: "Party Games", 0: "Anime", 1: "Horror", 2: "Mystery", 3: "Science-fiction",
                    4: "Fantasy", 5: "Post-apocalyptic", 6: "History", 7: "Modern", 8: "War", 9: "Superhero"}

    if isinstance(key, int):
        definition = backward_map.get(key)
    else:
        definition = forward_map.get(key)
    return definition
