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

import string

import spacy
from sklearn.base import TransformerMixin

# Build a list of stopwords to use to filter
nlp = spacy.load("en_core_web_sm")
wh_words = ["what", "where", "which", "why", "who", "how", "or"]
punctuations = string.punctuation

# Function to clean the text
def clean_text(text):
    return text.strip().lower()


# Function to tokenize text
def query_tokenizer(sentence):
    mytokens = nlp(sentence)
    tokens = []
    for token in mytokens:
        if (
            (not token.is_stop and not token.is_punct)
            or (token.pos_ == "ADJ")
            or (token.text.lower() in wh_words)
        ):
            tokens.append(str(token.lemma_).lower())
    return tokens


# Class for text transformation
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        return [clean_text(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}


# Function to convert scraped data to HTML format
def create_html_bracket(bracket_map):
    west = [bracket_map["Western Conference First Round"]]
    east = [bracket_map["Eastern Conference First Round"]]
    finals = []

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
        "wc1": west[0],
        "wc2": west[1],
        "wcf": west[2],
        "ec1": east[0],
        "ec2": east[1],
        "ecf": east[2],
        "f": finals,
    }

    return playoff_map


# Function to build HTML level for playoff bracket
def build_level(prev, bracket, conf):

    level_map = {
        "4west": "Western Conference Semifinals",
        "4east": "Eastern Conference Semifinals",
        "2west": "Western Conference Finals",
        "2east": "Eastern Conference Finals",
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
        high = len(next) - 1
        while low < high:
            vs = [next[low], next[high]]
            level.append(vs)
            low += 1
            high -= 1
    else:
        i = 0
        while i < len(next):
            vs = [next[i], next[i + 1]]
            level.append(vs)
            i += 2

    return level
