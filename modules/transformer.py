import string
import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.base import TransformerMixin

# Build a list of stopwords to use to filter
nlp = spacy.load('en')
stopwords = list(STOP_WORDS)
punctuations = string.punctuation
parser = English()

# Function to clean the text 
def clean_text(text):     
    return text.strip().lower()

# Function to tokenize text 
def query_tokenizer(sentence):
    mytokens = parser(sentence)
    mytokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens]
    mytokens = [word for word in mytokens if word not in stopwords and word not in punctuations]
    return mytokens

# Class for text transformation
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        return [clean_text(text) for text in X]
    def fit(self, X, y=None, **fit_params):
        return self
    def get_params(self, deep=True):
        return {}

def create_html_bracket(bracket_map):
    # TODO
    return 0