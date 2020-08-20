import pickle
import string
import pandas as pd

# NLP packages 
import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

# ML packages
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score 
from sklearn.base import TransformerMixin 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer



# Build a list of stopwords to use to filter
nlp = spacy.load('en')
stopwords = list(STOP_WORDS)
punctuations = string.punctuation
parser = English()

# Class for text transformation
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        return [clean_text(text) for text in X]
    def fit(self, X, y=None, **fit_params):
        return self
    def get_params(self, deep=True):
        return {}

# Function to clean the text 
def clean_text(text):     
    return text.strip().lower()

# Function to tokenize text 
def query_tokenizer(sentence):
    mytokens = parser(sentence)
    mytokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens]
    mytokens = [word for word in mytokens if word not in stopwords and word not in punctuations]
    return mytokens

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
    print("Accuracy:", pipe.score(X_test,y_test))
    return pipe

def main():
    # Build model 
    query_classifier = create_pipeline()
    model_file = "./models/query_classifier.sav"
    pickle.dump(query_classifier, open(model_file, "wb"))

if __name__ == "__main__":
    main()