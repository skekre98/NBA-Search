import warnings
import pandas as pd
from modules.transformer import predictors, query_tokenizer
warnings.filterwarnings(action='ignore', category=FutureWarning)

# ML packages
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score  
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Load query dataset 
def read_data():
    return pd.read_csv("./data/query.csv")

# Function to build NLP pipeline
def create_pipeline():
    # Vectorization
    tfvectorizer = TfidfVectorizer(tokenizer=query_tokenizer) 
    classifier = LinearSVC()

    # Create the  pipeline to clean, tokenize, vectorize, and classify with TF Vectorization
    pipe = Pipeline([("cleaner", predictors()),
                    ('vectorizer', tfvectorizer),
                    ('classifier', classifier)])
    
    # Load dataset 
    df = read_data()
    X = df['Query']
    ylabels = df['Class']
    X_train, X_test, y_train, y_test = train_test_split(X, ylabels, test_size=0.2, random_state=42)

    # Fit our data
    pipe.fit(X_train,y_train)
    print("Query Classifier Training Accuracy:", pipe.score(X_test,y_test))
    return pipe

def main():
    # Train model 
    print("Training Query Classifier...")
    query_classifier = create_pipeline()
    joblib.dump(query_classifier, "./inference/models/query_classifier.pkl")

if __name__ == "__main__":
    main()