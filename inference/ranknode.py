import random
import spacy
from difflib import SequenceMatcher
from modules.scraper import get_adv_stat

inc_names = "Seems I couldn't extract players for ranking, try writing your question more verbosely. "
inc_names += "My grasp on the English language still needs a little improvement..."
inc_metric = "Seems I couldn't extract the metric for ranking, try writing your question more verbosely. "
inc_metric += "My grasp on the English language still needs a little improvement..."
inc_stat = "Seems I was unable to isolate the required statistics necessary for ranking, "
inc_stat += "try writing your quesion more verbosely."
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

	def __init__(self, query):
		self.query = query
		self.nlp = spacy.load('en_core_web_sm')

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

		value_1 = self.get_stat(name_1, metric)
		value_2 = self.get_stat(name_2, metric)
		entity_1 = (name_1, value_1) 
		entity_2 = (name_2, value_2)

		better_player = lambda a, b : a if a[1] > b[1] else b
		max_entity = better_player(entity_1, entity_2)

		resp_1 = "{} has performed better in the past with a {} of {}.".format(max_entity[0], stat, max_entity[1])
		resp_2 = "Statistically speaking {} is superior with a {} of {}.".format(max_entity[0], stat, max_entity[1])
		resp_3 = "With a {} of {} I'd have to go with {}. It's alright if you have a different opinion as long as you don't mind being wrong.".format(stat, max_entity[1], max_entity[0])
		resp_list = [resp_1, resp_2, resp_3]
		return random.choice(resp_list)

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