"""
House Price Prediction Model
This script loads the housing dataset, preprocesses the data,
trains a Linear Regression model, and saves it using pickle.
"""

# Import required libraries
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

print("=" * 60)
print("HOUSE PRICE PREDICTION MODEL - TRAINING")
print("=" * 60)

# Step 1: Load the dataset
print("\n[STEP 1] Loading dataset...")
try:
    data = pd.read_csv('dataset.csv')
    print(f"✓ Dataset loaded successfully!")
    print(f"  Shape: {data.shape[0]} rows, {data.shape[1]} columns")
except FileNotFoundError:
    print("✗ Error: dataset.csv not found!")
    exit()

# Step 2: Display dataset information
print("\n[STEP 2] Exploring dataset...")
print(f"\nFirst few rows of the dataset:")
print(data.head())
print(f"\nDataset Info:")
print(data.info())
print(f"\nStatistical Summary:")
print(data.describe())

# Step 3: Data Preprocessing - Handle missing values
print("\n[STEP 3] Data Preprocessing...")
print(f"Missing values before cleaning:")
print(data.isnull().sum())

# Fill missing values with mean (if any)
data = data.fillna(data.mean())
print(f"Missing values after cleaning:")
print(data.isnull().sum())

# Remove duplicates (if any)
initial_rows = len(data)
data = data.drop_duplicates()
removed_duplicates = initial_rows - len(data)
if removed_duplicates > 0:
    print(f"✓ Removed {removed_duplicates} duplicate rows")
else:
    print(f"✓ No duplicate rows found")

# Step 4: Prepare features and target variable
print("\n[STEP 4] Preparing features and target variable...")
X = data[['area', 'bedrooms', 'bathrooms', 'stories', 'parking']]
y = data['price']

print(f"Features (X) shape: {X.shape}")
print(f"Target (y) shape: {y.shape}")
print(f"Feature columns: {list(X.columns)}")
print(f"Target column: price")

# Step 5: Split dataset into training and testing sets
print("\n[STEP 5] Splitting dataset into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"✓ Training set size: {X_train.shape[0]} samples (80%)")
print(f"✓ Testing set size: {X_test.shape[0]} samples (20%)")

# Step 6: Train the Linear Regression model
print("\n[STEP 6] Training Linear Regression model...")
model = LinearRegression()
model.fit(X_train, y_train)
print(f"✓ Model trained successfully!")

# Step 7: Display model coefficients
print(f"\n[STEP 7] Model Coefficients:")
print(f"{'Feature':<15} {'Coefficient':>15}")
print("-" * 30)
for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature:<15} {coef:>15.2f}")
print(f"{'Intercept':<15} {model.intercept_:>15.2f}")

# Step 8: Make predictions on test set
print("\n[STEP 8] Making predictions on test set...")
y_pred = model.predict(X_test)
print(f"✓ Predictions generated for {len(y_pred)} test samples")

# Step 9: Evaluate model performance
print("\n[STEP 9] Model Evaluation Metrics:")
print("=" * 60)

# Calculate accuracy (R² score)
r2 = r2_score(y_test, y_pred)
print(f"R² Score (Accuracy):        {r2:.4f} ({r2*100:.2f}%)")

# Calculate Mean Absolute Error
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error (MAE):  ${mae:,.2f}")

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error (MSE):   ${mse:,.2f}")

# Calculate Root Mean Squared Error
rmse = np.sqrt(mse)
print(f"Root Mean Squared Error:    ${rmse:,.2f}")

print("=" * 60)

# Step 10: Display sample predictions
print("\n[STEP 10] Sample Predictions:")
print(f"{'Actual Price':>15} {'Predicted Price':>18} {'Difference':>15}")
print("-" * 50)
for i in range(min(5, len(y_test))):
    actual = y_test.iloc[i]
    predicted = y_pred[i]
    diff = actual - predicted
    print(f"${actual:>14,.0f} ${predicted:>17,.0f} ${diff:>14,.0f}")

# Step 11: Save the trained model using pickle
print("\n[STEP 11] Saving trained model...")
try:
    with open('house_price_model.pkl', 'wb') as file:
        pickle.dump(model, file)
    print(f"✓ Model saved successfully as 'house_price_model.pkl'")
except Exception as e:
    print(f"✗ Error saving model: {e}")

# Step 12: Verify the saved model
print("\n[STEP 12] Verifying saved model...")
try:
    with open('house_price_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    print(f"✓ Model loaded successfully from pickle file")
    
    # Test with a sample prediction
    sample = np.array([[2600, 4, 3, 2, 2]])
    sample_pred = loaded_model.predict(sample)[0]
    print(f"✓ Test prediction: ${sample_pred:,.2f}")
except Exception as e:
    print(f"✗ Error loading model: {e}")

print("\n" + "=" * 60)
print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nNext Steps:")
print("1. The trained model has been saved as 'house_price_model.pkl'")
print("2. Run 'python app.py' to start the Flask web application")
print("3. Open your browser and navigate to 'http://localhost:5000'")
print("4. Enter house features to predict the price")
print("=" * 60)
