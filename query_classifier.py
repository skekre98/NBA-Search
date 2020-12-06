# Copyright (c) 2020 Sharvil Kekre skekre98
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import warnings

import pandas as pd

from modules.transformer import predictors, query_tokenizer

warnings.filterwarnings(action="ignore", category=FutureWarning)

from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
# ML packages
from sklearn.svm import LinearSVC


# Load query dataset
def read_data():
    return pd.read_csv("./data/query.csv")


# Function to build NLP pipeline
def create_pipeline():
    # Vectorization
    tfvectorizer = TfidfVectorizer(tokenizer=query_tokenizer)
    classifier = LinearSVC()

    # Create the  pipeline to clean, tokenize, vectorize, and classify with TF Vectorization
    pipe = Pipeline(
        [
            ("cleaner", predictors()),
            ("vectorizer", tfvectorizer),
            ("classifier", classifier),
        ]
    )

    # Load dataset
    df = read_data()
    X = df["Query"]
    ylabels = df["Class"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, ylabels, test_size=0.2, random_state=42
    )

    # Fit our data
    pipe.fit(X_train, y_train)
    print("Query Classifier Training Accuracy:", pipe.score(X_test, y_test))
    return pipe


def main():
    # Train model
    print("Training Query Classifier...")
    query_classifier = create_pipeline()
    joblib.dump(query_classifier, "./inference/models/query_classifier.pkl")


if __name__ == "__main__":
    main()
