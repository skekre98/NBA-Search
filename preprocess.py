# script to preprocess data into balanced dataset or generate data
import json
from random import choice, randint
from modules.scraper import get_player_names
from data.text_data import percent_list

# Function to generate randomized instance of name 
def funnel_name(name):
    inst = randint(1, 3)
    name_split = name.split()
    if inst == 1:
        return name_split[0].lower()
    elif inst == 2:
        return name_split[1].lower()
    else:
        return name.lower()

# Function to generate rank queries 
def generate_rank_queries(samples):
    names = get_player_names(2020)
    stat_list = ["shoot", "rebound", "steal", "assist", "throw", "catch", "play"]
    cnt = 0
    query_list = []
    while cnt < samples:
        randq = randint(0, 4)
        if randq == 0:
            name1 = funnel_name(choice(names))
            name2 = funnel_name(choice(names))
            stat = choice(stat_list)
            query = "who is a better {}er between {} and {}, 1\n".format(stat, name1, name2)
            query_list.append(query)
        elif randq == 1:
            name1 = funnel_name(choice(names))
            name2 = funnel_name(choice(names))
            query1 = "could {} beat {} in 1v1, 1\n".format(name1, name2)
            query2 = "could {} beat {} in one on one, 1\n".format(name1, name2)
            query3 = "could {} beat {} in basketball, 1\n".format(name1, name2)
            Qs = [query1, query2, query3]
            query_list.append(choice(Qs))
        elif randq == 2:
            name1 = funnel_name(choice(names))
            name2 = funnel_name(choice(names))
            stat = choice(stat_list)
            query1 = "who is better at {}ing {} or {}, 1\n".format(stat, name1, name2)
            query2 = "is {} or {} better at {}ing, 1\n".format(name1, name2, stat)
            Qs = [query1, query2]
            query_list.append(choice(Qs))
        elif randq == 3:
            name1 = funnel_name(choice(names))
            name2 = funnel_name(choice(names))
            query1 = "should I pick {} or {}, 1\n".format(name1, name2)
            query2 = "should I put {} or {} on my fantasy team, 1\n".format(name1, name2)
            query3 = "who should I pick for fantasy, 1\n"
            Qs = [query1, query2, query3]
            query_list.append(choice(Qs))
        else:
            # The goat query
            goats = ["Michael Jordan", "Kobe Bryant", "Lebron James", "Magic Johnson", "Larry Bird"]
            name1 = funnel_name(choice(goats))
            name2 = funnel_name(choice(goats))
            query = "{} or {}, 1\n".format(name1, name2)
            query_list.append(query)
        cnt += 1
    
    return query_list

# Function to generate stat queries 
def generate_stat_queries(samples):
    names = get_player_names(2020)
    stat_list = ["shot", "rebound", "steal", "assist", "turnover", "point"]
    cnt = 0
    query_list = []
    while cnt < samples:
        randq = randint(0, 6)
        if randq < 5:
            name = funnel_name(choice(names))
            action = choice(stat_list)
            query1 = "how many {}s does {} put up, 2\n".format(action, name)
            query2 = "how many {}s does {} have per game, 2\n".format(action, name)
            query3 = "how many {}s did {}, 2\n".format(action, name)
            Qs = [query1, query2, query3]
            query_list.append(choice(Qs))
        elif randq == 5:
            action = choice(stat_list)
            query1 = "who is the best {}er in the league, 2\n".format(action)
            query2 = "who is the worst {}er there is, 2\n".format(action)
            query3 = "who has the most {}s per game, 2\n".format(action)
            query4 = "who is the best {}er, 2\n".format(action)
            Qs = [query1, query2, query3, query4]
            query_list.append(choice(Qs))
        elif randq == 6:
            stat = choice(percent_list)
            query1 = "who has the highest {} percentage in the nba, 2\n".format(action)
            query2 = "who has the highest {} percentage, 2\n".format(action)
            query3 = "who has the best {}{}, 2\n".format(action, "%")
            query4 = "who has the highest {}{} around, 2\n".format(action, "%")
            Qs = [query1, query2, query3, query4]
            query_list.append(choice(Qs))
        cnt += 1
    
    return query_list

def main():

    ranked_queries = generate_rank_queries(1500)
    stat_queries = generate_stat_queries(1500)
    query_csv = open("data/query.csv", "a")
    for i in range(1500):
        query_csv.write(stat_queries[i])
        query_csv.write(ranked_queries[i])
    query_csv.close()
if __name__ == "__main__":
    main()