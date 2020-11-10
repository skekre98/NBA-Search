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

	def random_be_response(Self):
		"""
		Function returns random response from 10 premade responses for be or do questions. This function works
		in conjuction with the generate_random_response.
		----------
		input : None
		-------
		Returns
		output : Random response.
			The response is a string.
		"""
		resp_1 = "I'm an NBA search bot, here to answer your NBA queries."
		resp_2 = "I'm a chatbot here to answer your questions."
		resp_3 = "I'm just some lines of code trying to decipher what you asked me in a different language via math and natural language processing."
		resp_4 = "I am a robot! I run on so many lines of code, and I am ready to answer your NBA queries."
		resp_5 = "I am actually a human that lives inside a computer that runs on code. Wait, thats a robot. I am a robot."
		resp_6 = "Bot, chatbot, robot, wizard. Those are all the things I've been described as. I can answer NBA questions for you."
		resp_7 = "I may be a robot. I may be a person. You'll never know, but I am here to answer your NBA questions."
		resp_8 = "I'm an NBA wizard ready to answer your NBA questions."
		resp_9 = "I'm like santa clause, but I deliver NBA knowledge."
		resp_10 = "Right now, I am a robot powered by machine learning. In 5 years, I want to be an ESPN commentator. Anyway, ask me something about the NBA."
		
		responses = [resp_1, resp_2, resp_3, resp_4, resp_5, resp_6, resp_7, resp_8, resp_9, resp_10]
	
		return random.choice(responses)

	def random_make_response(self):
		"""
		Function returns random response from 10 premade responses for be or do questions. This function works
		in conjuction with the generate_random_response.
		----------
		input : None
		-------
		Returns
		output : Random response.
			The response is a string.
		"""
		resp_1 = "I'm an NBA search bot, here to answer your NBA queries."
		resp_2 = "I'm a bot made by skekre98 in 2020, waiting for you to ask me real questions!"
		resp_3 = "I was built by skekre98 and the open source community in 2020!"
		resp_4 = "2020 was crazy! But, its the same year that I was started by skekre98."
		resp_5 = "I am constantly growing, thanks to the open source community on GitHub."
		resp_6 = "Honestly, I did not even know I was being built, until skekre98 and the open source community told me."
		resp_7 = "That is confidental information. Just kidding, I am being built by the open source community."
		resp_8 = "I am smart. Not because of the knowledge I have, but because my backer is the GitHub open source community."
		resp_9 = "Built and designed by skekre98, and the open source community on GitHub."
		resp_10 = "I am being built by the open source community, and skekre98 is leading them."
  
		responses = [resp_1, resp_2, resp_3, resp_4, resp_5, resp_6, resp_7, resp_8, resp_9, resp_10]
		return random.choice(responses)

	def generate_random_response(self, lemma, test=False):
		if 'do' in lemma or 'be' in lemma:
			if test:
				return({'do','be'})
			else:
				return self.random_be_response()

		elif 'make' in lemma or 'build' in lemma:
			if test:
				return({'make','build'})
			else:
				return self.random_make_response()

		else:
			if test:
				return 'Cannot Understand'
			else:
				return "I'm not sure what you're asking me. Can you be more clear?"
