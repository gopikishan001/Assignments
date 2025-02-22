import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Step 1: Reading the file
data = pd.read_excel('Rotten_Tomatoes_Movies3.xls')

# Step 2: Data Cleaning
# Dropping columns with excessive missing values (>50% missing as an example)
data_cleaned = data.dropna(thresh=len(data) * 0.5, axis=1)

# Imputing missing values for numeric columns
numeric_columns = data_cleaned.select_dtypes(include=['float64', 'int64']).columns
imputer = SimpleImputer(strategy='median')
data_cleaned.loc[:, numeric_columns] = imputer.fit_transform(data_cleaned[numeric_columns])

# Converting date columns to datetime
data_cleaned['in_theaters_date'] = pd.to_datetime(data_cleaned['in_theaters_date'], errors='coerce')

# Extracting year from 'in_theaters_date'
data_cleaned.loc[:, 'release_year'] = data_cleaned['in_theaters_date'].dt.year

data_cleaned['rating'] = pd.factorize(data_cleaned['rating'])[0]
data_cleaned['tomatometer_status'] = pd.factorize(data_cleaned['tomatometer_status'])[0]
data_cleaned['studio_name'] = pd.factorize(data_cleaned['studio_name'])[0]

# Step 3: Splitting the 'genre' column into individual categories
# Split the 'genre' column into lists

for x in ['genre', 'cast' , 'writers', 'directors'] :
    data_cleaned[x] = data_cleaned[x].apply(lambda x: str(x).split(', '))
    data_cleaned[x] = data_cleaned[x].apply(lambda x: len(x))

# Step 4: Defining features and target
X = data_cleaned.drop(columns=[ 'audience_rating', 'movie_title', 'movie_info', 'critics_consensus', 
                                'in_theaters_date', 'on_streaming_date', 


    # 'tomatometer_rating',
     'runtime_in_minutes',
      'release_year' , 
      # 'tomatometer_count' , 
      'studio_name',
    'cast', 
    'rating', 
    # 'genre', 
    'writers', 
    'tomatometer_status',
    'directors',


                                ], errors='ignore')
y = data_cleaned['audience_rating']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Preprocessing
# Imputing missing values for numeric features in training and test data
for col in X_train.select_dtypes(include=['float64', 'int64']).columns:
    imputer = SimpleImputer(strategy='median')
    X_train.loc[:, col] = imputer.fit_transform(X_train[[col]])
    X_test.loc[:, col] = imputer.transform(X_test[[col]])

# Scaling numeric features
scaler = StandardScaler()
numeric_features = ['tomatometer_rating', 'tomatometer_count']
X_train.loc[:, numeric_features] = scaler.fit_transform(X_train[numeric_features])
X_test.loc[:, numeric_features] = scaler.transform(X_test[numeric_features])

# Step 6: Model Training
model = RandomForestRegressor(random_state=42)

# print(X_train)
model.fit(X_train, y_train)

# # Saving the model
# joblib.dump(model, 'audience_rating_model_with_genres.pkl')

# Step 7: Prediction and Validation
y_pred = model.predict(X_test)

# Validation Metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

print("Validation Metrics:")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R-squared (R2): {r2}")

# Step 8: Feature Importance Analysis
feature_importances = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nTop Features by Importance:")
print(feature_importances.head(10))
