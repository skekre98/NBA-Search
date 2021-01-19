import spacy
import random
from modules.scraper import get_adv_stat, get_total_stat
from data.text_data import adv_stat_map, total_stat_map
from fuzzywuzzy import fuzz, process

inc_name = "Seems I couldn't extract the name for retrieval, try writing your question more verbosely. "
inc_name += "Unfortunately, English is not my native language..."
inc_stat = "Seems I couldn't extract the statistic for retrieval, try writing your question more verbosely. "
inc_stat += "Can you really blame me? English is not my first language..."


class StatNode(object):

    def __init__(self):
        self.query = ""
        self.nlp = spacy.load("en_core_web_md")

    def load_query(self, query):
        self.query = query

    """
    Function to get a list of a random_response. 
    
    Parameters
    ----------
    stat : string
        The stat that is being compared to stat_val
    name : string
        NBA player for stat retrieval
    stat_val: string
        statistic value
    
    Returns
    -------
    resp_list : list
        The list of random response
    """

    def generate_random_response(self, name, stat, stat_val):
        resp_1 = "Seems {} has an {} out of {}.".format(name, stat, stat_val)
        resp_2 = "After checking my little black book, I've found that {} has {} under his name for {}.".format(name,
                                                                                                                stat_val,
                                                                                                                stat)
        resp_3 = "{}...obviously".format(stat_val)
        resp_4 = "Last I checked... {} had a {} out of {}.".format(name, stat, stat_val)
        resp_5 = "Do you not have every NBA stat since the beginning of time memorized? Well, he has a {} out of {}.".format(
            stat, stat_val)
        resp_6 = "{} has {} out of {}, impressive isn't it?".format(name, stat, stat_val)
        resp_7 = "As we are speaking, {} has {} out of {}".format(name, stat, stat_val)
        resp_8 = "After watching hours of tapes, I came up with {} out of {} for {}".format(stat, stat_val, name)
        resp_9 = "If my calculations are correct {} has {} out of {} during his career".format(name, stat, stat_val)
        resp_10 = "Couldn't you Google that? Well since we're already here: {} has {} out of {}".format(name, stat,
                                                                                                        stat_val)
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

    """
        Function to generate a response
        
        Parameters
        ----------
        self : none
            
        
        Returns
        -------
        name : string
          NBA player for stat retrieval
        stat : string
          The stat that is being compared to stat_val
        stat_val : string
          statistic value
    """

    def response(self):
        name = self.extract_name()
        stat = self.extract_stat()
        if not name:
            return inc_name
        elif not stat:
            return inc_stat
        stat_val = self.get_player_stat(name, stat)
        return self.generate_random_response(name, stat, stat_val)

    """
        Function that extracts the player's name
        
        Parameters
        ----------
        self : none
            
        Returns
        -------
        name : string
          NBA player for stat retrieval
    """

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

    """
    Function that extracts the player's statistics
    Parameters
    ----------
    self : none

    Returns
    -------
    stat_final : string
        Player statistics
    or None
    """

    def extract_stat(self):
        doc = self.nlp(self.query)
        stat = ""
        stat_final = ""
        sim_threshold = 50

        # preprocessing user query and choosing the most ocurring word classes in statistics dictionary
        for token in doc:

            if token.pos_ == "ADJ" or token.pos_ == "VERB" or token.pos_ == "NOUN" or token.pos_ == "NUM" or token.text == "per" or token.pos_ == "SYM" or token.pos_ == "CCONJ":
                stat = str(stat) + token.text + " "
        stat = stat[:-1]

        # checking if there is an exaxt match in dictionary, in order to save some time and avoid similarity prediction
        for entry, entry2 in zip(total_stat_map, adv_stat_map):
            if entry == stat or entry2 == stat:
                stat_final = stat
        if stat_final != "":
            return stat_final

        # if no exact match was found, use fuzzy string matching to find a close match
        # create lists out of stat maps' keys
        stat_map1 = total_stat_map.keys()
        stat_map2 = adv_stat_map.keys()

        # extract fuzzy matches from total and adv stat maps, compare which is closer and return
        # 'doc' gives better results than 'stat', worth continuing to look into
        stat_total, ratio_total = process.extractOne(str(doc), stat_map1)
        stat_adv, ratio_adv = process.extractOne(str(doc), stat_map2)
        # if neither ratio is higher than the similarity threshold, return None
        if ratio_total < sim_threshold and ratio_adv < sim_threshold:
            return None
        elif ratio_total > ratio_adv:
            return stat_total
        else:
            return stat_adv
    """
      Function to get player statistics
    
        Parameters
        ----------
        self : none
        stat : string
          The stat that is being compared to stat_val
        name : string
          NBA player for stat retrieval    
    
        Returns
        -------
        val : string
          statistic value
    """
    def get_player_stat(self, name, stat):
        if stat in total_stat_map:
            val = get_total_stat(name, stat)
        else:
            val = get_adv_stat(name, stat)
        return val




