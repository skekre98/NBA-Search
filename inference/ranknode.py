import random
import spacy
from difflib import SequenceMatcher
from modules.scraper import get_adv_stat

inc_names = "Seems I couldn't extract players for ranking, try writing your question more verbosely. "
inc_names += "My grasp on the English language still needs a little improvement..."
inc_metric = "Seems I couldn't extract the metric for ranking, try writing your question more verbosely. "
inc_metric += "My grasp on the English language still needs a little improvement..."
inc_stat = "Seems I was unable to isolate the required statistics necessary for ranking, "
inc_stat += "try writing your quesion more verbosely. "
inc_stat += "My grasp on the English language still needs a little improvement..."

metric_map = {
	"true shooting percentage" : ["shooting", "shooter"],
	"total rebound percentage" : ["rebounder", "rebounding"],
	"defensive plus/minus" : ["defender", "defending"],
	"offensive plus/minus" : ["scorer", "scoring"],
	"player efficiency rating" : ["player", "playing"],
	"assist percentage" : ["maker", "assisting", "passer", "passing"]
}

class RankNode(object):

	def __init__(self):
		self.query = ""
		self.nlp = spacy.load('en_core_web_sm')

	def load_query(self, query):
		self.query = query

	def response(self):
		name_1, name_2 = self.extract_names()
		if not name_1 or not name_2:
			return inc_names
		metric = self.extract_metric()
		if not metric:
			return inc_metric
		stat = self.metric2stat(metric)
		if not stat:
			return inc_stat

		value_1 = self.get_stat(name_1, stat)
		value_2 = self.get_stat(name_2, stat)
		entity_1 = (name_1, value_1) 
		entity_2 = (name_2, value_2)

		better_player = lambda a, b : (a, b) if a[1] > b[1] else (b, a)
		(max_entity, min_entity) = better_player(entity_1, entity_2)
		return self.generate_random_response(max_entity, min_entity, stat)


	"""
	Function to get a random response given two player entities

	Parameters
	----------
	max_entity : string tuple
		The player with better stats (name, stat)
	min_entity : string tuple
		The player with worse stats (name, stat)
	stat : string
		The stat that is being compared
	
	Returns
	-------
	response : string
		The randomly selected and formatted response

	"""
	def generate_random_response(self, max_entity, min_entity, stat):		
		resp_1 = "{} has performed better in the past with a {} of {}.".format(max_entity[0], stat, max_entity[1])
		resp_2 = "Statistically speaking {} is superior with a {} of {}.".format(max_entity[0], stat, max_entity[1])
		resp_3 = "With a {} of {} I'd have to go with {}. It's alright if you have a different opinion as long as you don't mind being wrong.".format(stat, max_entity[1], max_entity[0])
		resp_4 = "I mean {} has a {} of {}, so I'm going to assume that was a rhetorical question...".format(max_entity[0], stat, max_entity[1])
		resp_5 = "Is that a trick question? {} has a {} of {} while {} only has a {} of {}.".format(max_entity[0], stat, max_entity[1], min_entity[0], stat, min_entity[1])
		resp_6 = "{} maintains a higher {} of {}.".format(max_entity[0], stat, max_entity[1])
		resp_7 = "{} of {}: {}, {} of {}: {}, {} wins!".format(stat.capitalize(), max_entity[0], max_entity[1], stat, min_entity[0], min_entity[1], max_entity[0])
		resp_8 = "How could you even question {}'s {} {}.".format(max_entity[0], max_entity[1], stat)
		resp_9 = "{}'s {} {} is trash compared to {}'s {} {}.".format(min_entity[0], min_entity[1], stat, max_entity[0], max_entity[1], stat)
		resp_10 = "{}'s {} {} blows {}'s {} {} out of the water.".format(max_entity[0], max_entity[1], stat, min_entity[0], min_entity[1], stat)
		resp_11 = "Easy answer: {}'s {} {} is just better.".format(max_entity[0], max_entity[1], stat)
		resp_12 = "{}'s {} {} is good... Once it reaches {}'s {} {}.".format(min_entity[0], min_entity[1], stat, max_entity[0], max_entity[1], stat)
		resp_13 = "{} has a higher {} at {} which is just {} more than {}.".format(max_entity[0], stat, max_entity[1], round(max_entity[1]-min_entity[1], 3), min_entity[0])
		resp_14 = "{} has to put in a bit more work before you can even think about comparing his {} {} to {}'s {} {}.".format(min_entity[0], min_entity[1], stat, max_entity[0], max_entity[1], stat)
		resp_15 = "Don't even try to compare {}'s {} with {}'s {} when {}'s is {} higher than {}'s".format(max_entity[0], stat, min_entity[0], stat, max_entity[0], round(max_entity[1]-min_entity[1], 3), min_entity[0])
		resp_list = [resp_1, resp_2, resp_3, resp_4, resp_5, resp_6, resp_7, resp_8, resp_9, resp_10, resp_11, resp_12, resp_13, resp_14, resp_15]
		return random.choice(resp_list)

	"""
	Function to get the name of a player and their org name

	Parameters
	----------
	n/a

	Returns
	-------
	player_name : string
		the name of a the player
	org_name : string
		the name of that player's org
	"""
	def extract_names(self):
		stack = [None, None]
		doc = self.nlp(self.query)
		for entity in doc.ents:
			if entity.label_ == "PERSON":
				stack.append(entity.text)
		if len(stack) < 4:
			for entity in doc.ents:
				if entity.label_ == "ORG":
					stack.append(entity.text)
		return stack[-1], stack[-2]
	
	"""
	Function to extract token
	Parameters
	----------
	n/a

	Returns
	-------
	token text : string
		matched metric 
	"""
	def extract_metric(self):
		metric_pos = [("NN", "NOUN"), ("VBG", "VERB")]
		doc = self.nlp(self.query)
		for token in doc:
			for tag, pos in metric_pos:
				if tag == token.tag_ and pos == token.pos_:
					return token.text 
		return None


	def metric2stat(self, metric):
		metric = metric.lower()
		max_similarity = lambda a, b : a if a[1] > b[1] else b
		max_stat = (None, 0,0)
		for stat in metric_map:
			for m2s in metric_map[stat]:
				ratio = SequenceMatcher(None, metric, m2s).ratio()
				if ratio > 0.8:
					curr_stat = (stat, ratio)
					max_stat = max_similarity(max_stat, curr_stat)
		return max_stat[0]
	
	def get_stat(self, name, stat):
		return get_adv_stat(name, stat)

