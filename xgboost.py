import xgboost as xgb
from sklearn.feature_extraction.text import TfidfVectorizer

# Define the data and the labels
data = ["this is a sample text", "xgboost is a powerful tool", "this is another example"]
labels = [0, 1, 0]

# Extract features using a TF-IDF vectorizer
vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(data)

# Convert the features to a dense matrix
features = features.toarray()

# Train the xgboost model
model = xgb.XGBClassifier()
model.fit(features, labels)