from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
from urllib.parse import urlparse

from flask import Flask, render_template
from spam.app import spam_blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register the spam blueprint
app.register_blueprint(spam_blueprint, url_prefix="/spam")

# Load the saved model and vectorizer
try:
    model = pickle.load(open('savedmodel.sav', 'rb'))
    vectorizer = pickle.load(open('vectorizer.sav', 'rb'))
    print("Model and vectorizer loaded successfully!")
except Exception as e:
    print(f"Error loading model or vectorizer: {e}")
    model, vectorizer = None, None


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    result = ''
    if request.method == 'POST':
        try:
            # Handle JSON data from the frontend
            data = request.get_json()
            url = data.get('url', '').strip()
            print(f"Received URL: {url}")

            if not url:
                return jsonify({"result": "Please enter a URL."})
            elif not is_valid_url(url):
                return jsonify({"result": "Invalid URL format."})
            elif model is None or vectorizer is None:
                return jsonify({"result": "Model or vectorizer not loaded."})

            # Transform the URL using the loaded vectorizer
            url_tfidf = vectorizer.transform([url])

            # Get probability predictions
            probabilities = model.predict_proba(url_tfidf)[0]
            phishing_percentage = probabilities[1] * 100
            clean_percentage = probabilities[0] * 100

            # Determine the result
            if phishing_percentage > clean_percentage:
                result = f" Suspicious URL ({phishing_percentage:.2f}% phishing)"
            else:
                result = f" Clean URL ({clean_percentage:.2f}% legitimate)"

            return jsonify({"result": result})

        except Exception as e:
            print(f"Prediction error: {e}")
            return jsonify({"result": f"An error occurred during prediction: {e}"})


if __name__ == '__main__':
    app.run(debug=True)


