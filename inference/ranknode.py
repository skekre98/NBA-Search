import random
import spacy

inc_names = "Seems I couldn't extract players for ranking, try writing the names more verbosely. "
inc_names += "My grasp on the English language still needs a little improvement..."
inc_metric = "Seems I couldn't extract players for ranking, try writing the names more verbosely. "
inc_metric += "My grasp on the English language still needs a little improvement..."

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
		stat_1 = self.get_stat(name_1, metric)
		stat_2 = self.get_stat(name_2, metric)
		entity_1 = (name_1, stat_1) 
		entity_2 = (name_2, stat_2)

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
					return token 
		return None
	
	def metric2stat(self, metric):
		# TODO
		return "shooting percentage"
	
	def get_stat(self, name, metric):
		# TODO 
		return random.randint(0, 10)