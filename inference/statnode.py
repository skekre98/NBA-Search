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
        self.nlp = spacy.load("en_core_web_md")

    def load_query(self, query):
        self.query = query

    def generate_random_response(self, name, stat, val):
        resp_1 = "Seems {} has a {} of {}.".format(name, stat, stat_val)
        resp_2 = "After checking my little black book, I've found that {} has {} under his name for {}.".format(name, stat_val, stat)
        resp_3 = "{}...obviously".format(stat_val)
        resp_4 = "Last I checked... {} had a {} of {}.".format(name, stat, stat_val)
        resp_5 = "Do you not have every NBA stat since the beginning of time memorized? Well he has a {} of {}.".format(stat, stat_val)
        resp_6 = "{} has {} of {}, impressive isn't it?".format(name, stat, stat_val)
        resp_7 = "As we are speaking, {} has {} of {}".format(name, stat, stat_val)
        resp_8 = "After watching hours of tapes, I came with {} of {} for {}".format(stat, stat_val, name)
        resp_9 = "If my calculations are correct {} has {} of {} during his career".format(name, stat, stat_val)
        resp_10 = "Couldn't you Google that? Well since we're already here: {} has {} of {}".format(name, stat, stat_val)
        resp_list = [resp_1,
                     resp_2,
                     resp_3,
                     resp_4,
                     resp_5,
                     resp_6,
                     resp_7,
                     resp_8,
                     resp_9,
                     resp_10]
        return random.choice(resp_list)

    def response(self):
        name = self.extract_name()
        stat = self.extract_stat()
        stat_val = self.get_player_stat(name, stat)
        if not name:
            return inc_name
        elif not stat:
            return inc_stat
        return self.generate_random_response(name, stat, stat_val)


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
         doc = self.nlp(self.query)
         stat = ""
         stat_final = ""
         max_sim = 0
         sim_threshold = 0.7

         #preprocessing user query and choosing the most ocurring word classes in statistics dictionary
         for token in doc:
             if token.pos_ == "ADJ" or token.pos_ == "VERB" or token.pos_ == "NOUN" or token.pos_ == "NUM" or token.text == "per" or token.pos_ == "SYM" or token.pos_ == "CCONJ":
                 stat = str(stat) + token.text + " "
         stat = stat[:-1]

         #checking if there is an exaxt match in dictionary, in order to save some time and avoid similarity prediction
         for entry, entry2 in zip(total_stat_map, adv_stat_map):
             if entry == stat or entry2 == stat:
                 stat_final = stat
         if stat_final != "":
             return stat_final
     
         #if no exact match was found, we need to check similarity between stats and user query
         stat = self.nlp(stat)
         for entry in total_stat_map:
             entry = self.nlp(entry)
             sim = stat.similarity(entry)
             if max_sim < sim:
                 max_sim = sim
                 stat_final = entry #using stat_final because original variable stat is used to check similarity, so we can not change it

         for entry in adv_stat_map:
             entry = self.nlp(entry)
             sim = stat.similarity(entry)
             if max_sim < sim:
                 max_sim = sim
                 stat_final = entry
         
         #returning extracted stat if similarity exceeds minimum threshold
         if(max_sim > sim_threshold):
             return str(stat_final)
         return None
    
    def get_player_stat(self, name, stat):
        if stat in total_stat_map:
            val = get_total_stat(name, stat)
        else:
            val = get_adv_stat(name, stat)
        return val
