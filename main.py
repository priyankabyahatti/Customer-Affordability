from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, chi2, f_regression
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split, KFold, cross_validate, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.tree import DecisionTreeRegressor
import data_preprocessing as dp


def best_k_features(x, y, k):
    """ This Script selects top k important features from the dataset.
    Args:
        x: independent features
        y: dependent features
        k: k columns to be selected """
    select = SelectKBest(score_func=f_regression, k=k)
    z = select.fit_transform(x, y)
    filter = select.get_support()
    return filter


def evaluation_metrics(y_test, y_pred, x_train):
    """ This Script prints evaluation metrics performance of different regressors
    Args:
        y_test: actual target values
        y_pred: predicted target values
        x_train: independent features dataset """
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    n = len(x_train)
    p = 40
    actual_minus_predicted = sum((y_test - y_pred) ** 2)
    actual_minus_actual_mean = sum((y_test - y_test.mean()) ** 2)
    r2 = 1 - actual_minus_predicted / actual_minus_actual_mean
    adj_R2 = 1 - ((1 - r2) * (n - 1) / (n - p - 1))
    print('R²:', r2)
    print('Adjusted R²:', adj_R2)
    print(f'Mean absolute error: {mae:.2f}')
    print(f'Mean squared error: {mse:.2f}')
    print(f'Root mean squared error: {rmse:.2f}')


def main():
    """ Main function gets the data, splits it into train and test. Further, builds various regressors on top of the data
    and shows performance of various regressors """
    customer_df = dp.data_preprocess()
    X = customer_df.loc[:, customer_df.columns != 'affordability']
    y = customer_df['affordability']
    # k=15
    X = (X[X.columns[best_k_features(X, y, k=40)]])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

    pipelines = []

    pipelines.append(('Linear Regression', (Pipeline([('scaled', StandardScaler()), ('LR', LinearRegression())]))))
    pipelines.append(('Stochastic Gradient', (Pipeline([('scaled', StandardScaler()), ('SGD', SGDRegressor())]))))
    pipelines.append(('Decision Trees', (Pipeline([('scaled', StandardScaler()), ('DT', DecisionTreeRegressor())]))))
    pipelines.append(('Random Forests', (Pipeline([('scaled', StandardScaler()), ('RF', RandomForestRegressor())]))))
    pipelines.append(('KNN Regression', (Pipeline([('scaled', StandardScaler()), ('KNN', KNeighborsRegressor())]))))

    for pipe, model in pipelines:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print("=================================================")
        print(pipe)
        print("=================================================")
        # evaluation
        evaluation_metrics(y_test, y_pred, X_train)


if __name__ == '__main__':
    main()
