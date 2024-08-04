import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from backend.calculations.pothole_areas import get_pothole_area

def get_pothole_model(size, x1, x2):
    # Load the data from the Excel spreadsheet
    def load_data(file_path, sheet_name):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df


    # Split the data into features and target variable
    def split_data(df, target_column):
        X = df.drop(columns=[target_column])
        y = df[target_column]
        return X, y

    # Split the data into training and testing sets
    def split_train_test(X, y, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

    # Train the linear regression model
    def train_model(X_train, y_train):
        model = LinearRegression()
        model.fit(X_train, y_train)
        return model

    # Make predictions and evaluate the model
    def evaluate_model(model, X_test, y_test):
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        return mse, r2

    # Predict the target value for new data
    def predict_new_data(model, new_data):
        predictions = model.predict(new_data)
        return predictions
    
    # Adjust the intercept of the model
    def adjust_intercept(model, new_intercept):
        model.intercept_ = new_intercept
        return model
    
    #get full model
    def get_full_model(model, feature_names):
        coefficients = model.coef_
        intercept = model.intercept_
        model_info = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': coefficients
        })
        return model_info, intercept


    
    file_path = "backend/calculations/regModel/data/ModelData.xlsx"
    sheet_name = "PotholeD"  
    target_column = "cost"  
    
    # Load and preprocess data
    df = load_data(file_path, sheet_name)
    
    # Split data into features and target
    X, y = split_data(df, target_column)
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    mse, r2 = evaluate_model(model, X_test, y_test)
    # print(f"Mean Squared Error: {mse}")
    # print(f"R-squared: {r2}")
    
    # Get the full model
    feature_names = X.columns
    model_info, intercept = get_full_model(model, feature_names)
    #adjust_intercept(model, 0)
    # print("Model Coefficients:")
    # print(model_info)
    # print(f"Intercept: {intercept}")
    
    # Prepare new data for prediction
    new_data_dict = {
        'size': [size],
        'x1': [x1],
        'x2': [x2]
    }
    new_data = pd.DataFrame(new_data_dict)
    
    
    # Predict the target value for the new data
    predictions = predict_new_data(model, new_data)
    return predictions[0]
