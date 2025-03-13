import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the saved model and vectorizer
try:
    load_model = pickle.load(open('savedmodel.sav', 'rb'))
    vectorizer = pickle.load(open('vectorizer.sav', 'rb'))
    print("Model and vectorizer loaded successfully!")
except FileNotFoundError:
    print("Error: 'savedmodel.sav' or 'vectorizer.sav' file not found. Make sure both files are in the same directory.")
    exit()


# Function to predict if a URL is phishing or legitimate
def predict_url_with_loaded_model(url):
    try:
        # Transform input URL using the loaded vectorizer
        url_tfidf = vectorizer.transform([url])

        # Get probability predictions
        probabilities = load_model.predict_proba(url_tfidf)[0]

        # Extract percentages
        phishing_percentage = probabilities[1] * 100
        clean_percentage = probabilities[0] * 100

        # Display results
        if phishing_percentage > clean_percentage:
            return f"⚠️ Suspicious URL ({phishing_percentage:.2f}% phishing)"
        else:
            return f"✅ Clean URL ({clean_percentage:.2f}% legitimate)"

    except Exception as e:
        return f"An error occurred during prediction: {e}"


# Example: Test a new URL
input_url = input("Enter a URL to test with the loaded model: ")
result = predict_url_with_loaded_model(input_url)
print(result)

# Optional: Save vectorizer again if needed
# pickle.dump(vectorizer, open('vectorizer.sav', 'wb'))

# Let me know if you want me to add more error handling or test cases! 🚀
