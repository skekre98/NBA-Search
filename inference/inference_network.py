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

import pickle

from sklearn.externals import joblib

from data.text_data import non_nba, unsure
from inference.infonode import InfoNode
from inference.ranknode import RankNode
from inference.statnode import StatNode
from modules.analysis import isNBA
from modules.transformer import predictors, query_tokenizer


class InferenceNetwork(object):
    def __init__(self, query):
        self.query = query

        # Query classification
        model_file = "inference/models/query_classifier.pkl"
        query_clf = joblib.load(model_file)
        self.node_type = query_clf.predict([query.lower()])[0]

    def response(self):
        if self.node_type == "info":
            node = InfoNode()
        else:
            # Check if query is NBA related
            flag = isNBA(self.query)
            if flag == 0:
                return unsure
            elif flag == -1:
                return non_nba

            # Query is definitely NBA related
            if self.node_type == "rank":
                node = RankNode()

            if self.node_type == "stat":
                node = StatNode()

        node.load_query(self.query)
        return node.response()
