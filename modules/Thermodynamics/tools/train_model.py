from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import pandas as pd

def train_model(X, y, model_type='LinearRegression', alpha=1.0, scale=True):
    """
    Trains a regression model with preprocessing (imputation + scaling).

    Parameters:
        X (DataFrame): Input features
        y (Series): Target variable
        model_type (str): 'LinearRegression' or 'Ridge'
        alpha (float): Ridge regularization strength
        scale (bool): Whether to scale features

    Returns:
        model: Fitted pipeline
    """
    # Ensure input is a clean DataFrame
    X = pd.DataFrame(X)
    y = pd.Series(y)

    # Define imputer
    imputer = SimpleImputer(strategy='mean')

    # Define model
    regressor = Ridge(alpha=alpha) if model_type == 'Ridge' else LinearRegression()

    # Build pipeline
    steps = [('imputer', imputer)]
    if scale:
        steps.append(('scaler', StandardScaler()))
    steps.append(('regressor', regressor))

    model = Pipeline(steps)
    model.fit(X, y)

    return model
