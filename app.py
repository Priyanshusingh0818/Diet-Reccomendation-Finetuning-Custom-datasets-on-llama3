from flask import Flask, render_template, request, jsonify
import joblib
import os
from groq import Groq

app = Flask(__name__)

# Load the diet recommendation function
try:
    recommend_diet_with_llama = joblib.load('recommend_diet_with_llama.pkl')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    recommend_diet_with_llama = None

# Initialize Groq client (needed for the model to work)
os.environ["GROQ_API_KEY"] = "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"
client = Groq()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if recommend_diet_with_llama is None:
        return jsonify({"error": "Model not loaded properly"})
    
    try:
        # Get user input from form
        user_features = {
            'Age': int(request.form['age']),
            'Weight': float(request.form['weight']),
            'Height': float(request.form['height']),
            'Gender': request.form['gender'],
            'Activity': request.form['activity'],
            'Diet_current': request.form['diet_current'],
            'Goal': request.form['goal']
        }
        
        # Check for medical conditions and allergies
        conditions = request.form.getlist('conditions')
        allergies = request.form.getlist('allergies')
        
        if conditions:
            user_features['Medical_condition'] = ','.join(conditions)
        else:
            user_features['Medical_condition'] = 'None'
            
        if allergies:
            user_features['Allergies'] = ','.join(allergies)
        else:
            user_features['Allergies'] = 'None'
        
        # Get diet recommendation
        result = recommend_diet_with_llama(user_features)
        
        return render_template('result.html', 
                              recommendation=result,
                              user=user_features)
                              
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)