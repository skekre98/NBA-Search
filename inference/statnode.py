import spacy
import random
from modules.scraper import get_adv_stat, get_total_stat
from data.text_data import adv_stat_map, total_stat_map

inc_name = "Seems I couldn't extract the name for retrieval, try writing your question more verbosely. "
inc_name += "Unfortunately English is not my native language..."
inc_stat = "Seems I couldn't extract the statistic for retrieval, try writing your question more verbosely. "
inc_stat += "Can you really blame me? English is not my first language..."

class StatNode(object):

	def __init__(self):
		self.query = ""
		self.nlp = spacy.load("en_core_web_sm")

	def load_query(self, query):
		self.query = query

	def response(self):
		name = self.extract_entities()
		stat = self.extract_stat()
		if not name:
			return inc_name
		elif not stat:
			return inc_stat
		
		stat_val = self.get_player_stat(name, stat)
		resp_1 = "Seems {} has a {} of {}".format(name, stat, stat_val)
		resp_2 = "After checking my little black book, I've found that {} has {} under his name for {}".format(name, stat_val, stat)
		resp_3 = "{}...obviously".format(stat_val)
		resp_4 = "Last I checked... {} had a {} of {}".format(name, stat, stat_val)
		resp_5 = "Do you not have every NBA stat since the beginning of time memorized? Well he has a {} of {}".format(stat, stat_val)
		resp_list = [resp_1, resp_2, resp_3, resp_4, resp_5]
		return random.choice(resp_list)
	
	def extract_name(self):
		doc = self.nlp(self.query)
		name = None
		for entity in doc.ents:
			if entity.label_ == "PERSON":
				name = entity.text
		if not name:
			for entity in doc.ents:
				if entity.label_ == "ORG":
					name = entity.text

		return name
	
	def extract_stat(self):
		# TODO 
		return "field goal percentage"
	
	def get_player_stat(self, name, stat):
		if stat in total_stat_map:
			val = get_total_stat(name, stat)
		else:
			val = get_adv_stat(name, stat)
		return val