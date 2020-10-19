import random
import spacy
from difflib import SequenceMatcher

class InfoNode(object):

	def __init__(self):
		self.query = ""
		self.nlp = spacy.load('en_core_web_sm')

	def load_query(self, query):
		self.query = query

	def response(self):
		lemma = self.extract_components()
		return self.generate_random_response(lemma)

	def extract_components(self):
		verbs = []
		doc = self.nlp(self.query)
		for entity in doc:
			if entity.pos_ == "VERB" or entity.pos_ == "AUX":
				verbs.append(entity.lemma_)
		return verbs

	def generate_random_response(self, lemma):
		know_response = []
		make_response = []
		be_response = []
		resp_1 = "I'm an NBA search bot, here to answer your NBA queries"
		resp_2 = "I'm here to answer your questions, silly"
		resp_3 = "Waiting on you to send me a query to work with"
		know_response = [resp_1,resp_2,resp_3]
		resp_4 = "I was made by skekre98 in 2020, and I'm being built by the open source community on GitHub!"
		resp_5 = "I'm a bot made by skekre98 in 2020, waiting for you to ask me real questions!"
		resp_6 = "I was built by skekre98 and the open source community in 2020!"
		make_response = [resp_4,resp_5,resp_6]
		resp_7 = "I'm doing well, thanks for asking!"
		resp_8 = "Well and good"
		resp_9 = "Nothing much, waiting to be useful"
		be_response = [resp_7,resp_8,resp_9]

		if lemma == 'know':
			return random.choice(know_response)
		elif lemma == 'made':
			return random.choice(make_response)
		elif lemma == 'be':
			return random.choice(be_response)
		else:
			return "I'm not sure what you're asking me. Can you be more clear?"
