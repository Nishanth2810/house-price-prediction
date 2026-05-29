"""
House Price Prediction Web Application
Flask-based web application for predicting house prices using a trained ML model.
Users can input house features and get price predictions.
"""

# Import required libraries
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Initialize Flask application
app = Flask(__name__)

# Global variable to store the loaded model
model = None

def load_model():
    """
    Load the trained machine learning model from pickle file.
    Returns the loaded model or None if loading fails.
    """
    global model
    try:
        with open('house_price_model.pkl', 'rb') as file:
            model = pickle.load(file)
        print("[INFO] Model loaded successfully!")
        return True
    except FileNotFoundError:
        print("[ERROR] Model file 'house_price_model.pkl' not found!")
        print("[INFO] Please run 'python model.py' to train and save the model first.")
        return False
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")
        return False

def validate_input(area, bedrooms, bathrooms, stories, parking):
    """
    Validate user input to ensure all values are within acceptable ranges.
    
    Args:
        area (float): Total area of the house
        bedrooms (int): Number of bedrooms
        bathrooms (int): Number of bathrooms
        stories (int): Number of stories/floors
        parking (int): Number of parking spaces
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Convert inputs to appropriate types
        area = float(area)
        bedrooms = int(bedrooms)
        bathrooms = int(bathrooms)
        stories = int(stories)
        parking = int(parking)
        
        # Validate area
        if area <= 0 or area > 10000:
            return False, "Area must be between 1 and 10000 sq ft"
        
        # Validate bedrooms
        if bedrooms <= 0 or bedrooms > 10:
            return False, "Bedrooms must be between 1 and 10"
        
        # Validate bathrooms
        if bathrooms <= 0 or bathrooms > 10:
            return False, "Bathrooms must be between 1 and 10"
        
        # Validate stories
        if stories <= 0 or stories > 5:
            return False, "Stories must be between 1 and 5"
        
        # Validate parking
        if parking < 0 or parking > 10:
            return False, "Parking spaces must be between 0 and 10"
        
        return True, "Valid input"
    
    except ValueError:
        return False, "Please enter valid numeric values"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

@app.route('/')
def home():
    """
    Render the home page with the prediction form.
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests from the web form.
    
    Expected JSON data:
    {
        'area': float,
        'bedrooms': int,
        'bathrooms': int,
        'stories': int,
        'parking': int
    }
    
    Returns:
        JSON response with predicted price or error message
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Extract input values
        area = data.get('area')
        bedrooms = data.get('bedrooms')
        bathrooms = data.get('bathrooms')
        stories = data.get('stories')
        parking = data.get('parking')
        
        # Validate input
        is_valid, message = validate_input(area, bedrooms, bathrooms, stories, parking)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': message
            }), 400
        
        # Convert inputs to appropriate types
        area = float(area)
        bedrooms = int(bedrooms)
        bathrooms = int(bathrooms)
        stories = int(stories)
        parking = int(parking)
        
        # Check if model is loaded
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please restart the application.'
            }), 500
        
        # Prepare input for prediction (must match training features order)
        # Feature order: area, bedrooms, bathrooms, stories, parking
        input_data = np.array([[area, bedrooms, bathrooms, stories, parking]])
        
        # Make prediction
        predicted_price = model.predict(input_data)[0]
        
        # Ensure price is positive
        if predicted_price < 0:
            predicted_price = 0
        
        # Log the prediction
        print(f"[PREDICTION] Area: {area}, Beds: {bedrooms}, Baths: {bathrooms}, "
              f"Stories: {stories}, Parking: {parking} => Price: ${predicted_price:,.2f}")
        
        # Return successful prediction
        return jsonify({
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'formatted_price': f"${predicted_price:,.2f}"
        }), 200
    
    except Exception as e:
        print(f"[ERROR] Prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Prediction error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint to verify the application is running.
    """
    return jsonify({
        'status': 'running',
        'model_loaded': model is not None
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Page not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("HOUSE PRICE PREDICTION WEB APPLICATION")
    print("=" * 60)
    
    # Load the model before starting the application
    if load_model():
        print("[SUCCESS] Application initialized successfully!")
        print("=" * 60)
        print("\n[INFO] Starting Flask application...")
        print("[INFO] Open your browser and navigate to: http://localhost:5000")
        print("[INFO] Press Ctrl+C to stop the application")
        print("\n" + "=" * 60)
        
        # Run Flask application
        # debug=True enables auto-reload on code changes
        # Set to False in production
        app.run(debug=True, host='localhost', port=5000)
    else:
        print("[ERROR] Failed to initialize application!")
        print("[ERROR] Please train the model first by running: python model.py")
