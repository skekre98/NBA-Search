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
		verbs = set()
		doc = self.nlp(self.query)
		for entity in doc:
			if entity.pos_ == "VERB" or entity.pos_ == "AUX":
				verbs.add(entity.lemma_)
		return verbs

	def generate_random_response(self, lemma, test=False):
		resp_1 = "I'm an NBA search bot, here to answer your NBA queries."
		resp_2 = "I'm a chatbot here to answer your questions, obviously."
		resp_3 = "I'm just some lines of code trying to decipher what you asked me in a different language via math and natural language processing."
		be_response = [resp_1,resp_2,resp_3]
		resp_4 = "I was made by skekre98 in 2020, and I'm being built by the open source community on GitHub!"
		resp_5 = "I'm a bot made by skekre98 in 2020, waiting for you to ask me real questions!"
		resp_6 = "I was built by skekre98 and the open source community in 2020!"
		make_response = [resp_4,resp_5,resp_6]

		if 'do' in lemma or 'be' in lemma:
			if test:
				return(['do','be'])
			else:
				return random.choice(be_response)

		elif 'make' in lemma or 'build' in lemma:
			if test:
				return(['make','build'])
			else:
				return random.choice(make_response)

		else:
			if test:
				return 'Cannot Understand'
			else:
				return "I'm not sure what you're asking me. Can you be more clear?"
