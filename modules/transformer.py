import string
import spacy
from sklearn.base import TransformerMixin

# Build a list of stopwords to use to filter
nlp = spacy.load('en_core_web_sm')
wh_words = ['what','where','which','why','who','how','or']
punctuations = string.punctuation


"""
Function to clean the text, by
removing leading and trailing white space
and converting to lower case.

Parameters
----------
text : String
    Text to be cleaned.

Returns
-------
cleaned_text : String
    The cleaned text.
"""
def clean_text(text):     
    return text.strip().lower()

# Function to tokenize text

"""
Function to tokenize the text.

Parameters
----------
sentence : String
    The sentence to be tokenized.

Returns
-------
tokens : List
    List of words that are classified as token by nlp.
"""
def query_tokenizer(sentence):
    mytokens = nlp(sentence)
    tokens = []
    for token in mytokens:
        if (not token.is_stop and not token.is_punct) or (token.pos_ == 'ADJ') or (token.text.lower() in wh_words):
            tokens.append(str(token.lemma_).lower())
    return tokens

"""
A class which inherits from `sklearn.base.TransformerMixin<https://scikit-learn.org/stable/modules/generated/sklearn.base.TransformerMixin.html#sklearn.base.TransformerMixin>`.
It cleans the text to the format required.
"""
class predictors(TransformerMixin):
    """
    Function to clean a list of words.

    Parameters
    ----------
    X : List
        List of words to be clean.

    Returns
    -------
    cleaned_list : List
        List of clean words.
    """
    def transform(self, X, **transform_params):
        return [clean_text(text) for text in X]
    def fit(self, X, y=None, **fit_params):
        return self
    def get_params(self, deep=True):
        return {}

# Function to convert scraped data to HTML format
"""
Function to convert scraped data to HTML format.

Parameters
----------
bracket_map : Dictionary
    Dictionary of scraped data categorised into two key-value pairs, namely the "Western Conference First Round" and "Eastern Conference First Round".
    The function will convert the values from this two keys into HTML format.

Returns
-------
playoff_map : Dictionary
    Dictionary of the data in HTML format. 
    The dictionary will show the matchup for each series, and the number of wins during the series.
"""
def create_html_bracket(bracket_map):
    west = [bracket_map["Western Conference First Round"]]
    east = [bracket_map["Eastern Conference First Round"]]
    finals = []
    playoff_map = {}

    if not west[0] or not east[0]: # if returned scraped data is empty, need to return an empty map with correct fields
        empty_map = {
        "wc1" : [[("",""),("","")], [("",""),("","")], [("",""),("","")], [("",""),("","")]],
        "wc2" : [[("",""),("","")], [("",""),("","")]],
        "wcf" : [[("",""),("","")]],
        "ec1" : [[("",""),("","")], [("",""),("","")], [("",""),("","")], [("",""),("","")]],
        "ec2" : [[("",""),("","")], [("",""),("","")]],
        "ecf" : [[("",""),("","")]],
        "f" :   [("",""),("","")]
        }
        return empty_map

    for i in range(2):
        west_level = build_level(west[-1], bracket_map, "west")
        east_level = build_level(east[-1], bracket_map, "east")
        west.append(west_level)
        east.append(east_level)
    
    wf = west[-1][0]
    ef = east[-1][0]
    west_team = ""
    west_score = ""
    east_team = ""
    east_score = ""

    # Western Finalist 
    for team in wf:
        if team[1] == "4":
            west_team = team[0]
            if bracket_map["Finals"]:
                west_score = bracket_map["Finals"][0][0][1]
            break
    finals.append((west_team, west_score))

    # Eastern Finalist 
    for team in ef:
        if team[1] == "4":
            east_team = team[0]
            if bracket_map["Finals"]:
                east_score = bracket_map["Finals"][0][1][1]
            break
    finals.append((east_team, east_score))

    playoff_map = {
        "wc1" : west[0],
        "wc2" : west[1],
        "wcf" : west[2],
        "ec1" : east[0],
        "ec2" : east[1],
        "ecf" : east[2],
        "f" : finals
    }

    return playoff_map

"""
Function to build HTML level for playoff bracket 

Parameters
----------
bracket_map : Dictionary
    Dictionary of scraped data categorised into two key-value pairs, namely the "Western Conference First Round" and "Eastern Conference First Round".
    The function will convert the values from this two keys into HTML format.

prev : List
    List of the Series scored for the previous round.
    It should be one of the value in the `bracket` dictionary.

bracket : Dictionary
    Dictionary that contains the playoff informations, namely the match-up for each series and the number of wins for each team in the serires.
    This data has the following structure (*Note: # represents an integer stored as String):
        {
            Western First Round : [
                [
                    [Team A, #], [Team B, #] // Match-up and how many games won by each team.
                    :
                ]
            ],
            Western Second Round : [...], 
            Western Finals : [...],
            Eastern ...
        }

conf : String
    String with value "west" or "east" only.

Returns
-------
playoff_map : Dictionary
    Dictionary of the data in HTML format. 
    The dictionary will show the matchup for each series, and the number of wins during the series.
"""
def build_level(prev, bracket, conf):

    level_map = {
        "4west" : "Western Conference Semifinals",
        "4east" : "Eastern Conference Semifinals",
        "2west" : "Western Conference Finals",
        "2east" : "Eastern Conference Finals"
    }
    next = []
    for cell in prev:
        team = ""
        score = ""
        for t in cell:
            if t[0] != "" and t[1] == "4":
                team = t[0]
                key = str(len(prev)) + conf
                next_level = bracket[level_map[key]]
                for matchup in next_level:
                    for match in matchup:
                        if match[0] == team:
                            score = match[1]
                if score == "":
                    score = "0"
        next.append((team, score))
    
    level = []
    if conf == "east":
        low = 0
        high = len(next)-1
        while low < high:
            vs = [next[low], next[high]]
            level.append(vs)
            low += 1
            high -= 1
    else:
        i = 0
        while i < len(next):
            vs = [next[i], next[i+1]]
            level.append(vs)
            i += 2
    
    return level
