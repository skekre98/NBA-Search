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
        return name_split[0]
    elif inst == 2:
        return name_split[1]
    else:
        return name

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
            query = "who is a better {}er between {} and {},rank\n".format(stat, name1, name2)
            query_list.append(query)
        elif randq == 1:
            name1 = funnel_name(choice(names))
            name2 = funnel_name(choice(names))
            query1 = "could {} beat {} in 1v1,rank\n".format(name1, name2)
            query2 = "could {} beat {} in one on one,rank\n".format(name1, name2)
            query3 = "could {} beat {} in basketball,rank\n".format(name1, name2)
            Qs = [query1, query2, query3]
            query_list.append(choice(Qs))
        elif randq == 2:
            name1 = funnel_name(choice(names))
            name2 = funnel_name(choice(names))
            stat = choice(stat_list)
            query1 = "who is better at {}ing {} or {},rank\n".format(stat, name1, name2)
            query2 = "is {} or {} better at {}ing,rank\n".format(name1, name2, stat)
            Qs = [query1, query2]
            query_list.append(choice(Qs))
        elif randq == 3:
            name1 = funnel_name(choice(names))
            name2 = funnel_name(choice(names))
            query1 = "should I pick {} or {},rank\n".format(name1, name2)
            query2 = "should I put {} or {} on my fantasy team,rank\n".format(name1, name2)
            query3 = "who should I pick for fantasy,rank\n"
            Qs = [query1, query2, query3]
            query_list.append(choice(Qs))
        else:
            # The goat query
            goats = ["Michael Jordan", "Kobe Bryant", "Lebron James", "Magic Johnson", "Larry Bird"]
            name1 = funnel_name(choice(goats))
            name2 = funnel_name(choice(goats))
            query = "{} or {},rank\n".format(name1, name2)
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
        if randq < 2:
            name = funnel_name(choice(names))
            action = choice(stat_list)
            query1 = "how many {}s does {} put up,stat\n".format(action, name)
            query2 = "how many {}s does {} have per game,stat\n".format(action, name)
            query3 = "how many {}s did {},stat\n".format(action, name)
            Qs = [query1, query2, query3]
            query_list.append(choice(Qs))
        elif randq < 5:
            name = funnel_name(choice(names))
            action = choice(stat_list)
            query1 = "what is {}s {} percentage,stat\n".format(action, name)
            query2 = "what is {} {}s {},stat\n".format(name, action, "%")
            query3 = "what was {}s {} percentage in {},stat\n".format(action, name, str(randint(1988,2020)))
            query4 = "who had the best {} in {},stat\n".format(action, str(randint(1988,2020)))
            Qs = [query1, query2, query3, query4]
            query_list.append(choice(Qs))
        elif randq == 5:
            action = choice(stat_list)
            query1 = "who is the best {}er in the league,stat\n".format(action)
            query2 = "who is the worst {}er there is,stat\n".format(action)
            query3 = "who has the most {}s per game,stat\n".format(action)
            query4 = "who is the best {}er,stat\n".format(action)
            Qs = [query1, query2, query3, query4]
            query_list.append(choice(Qs))
        elif randq == 6:
            action = choice(stat_list)
            query1 = "who has the highest {} percentage in the nba,stat\n".format(action)
            query2 = "who has the highest {} percentage,stat\n".format(action)
            query3 = "who has the best {}{},stat\n".format(action, "%")
            query4 = "who has the highest {}{} around,stat\n".format(action, "%")
            Qs = [query1, query2, query3, query4]
            query_list.append(choice(Qs))
        cnt += 1
    
    return query_list

#function to generate info queries
def generate_info_queries(samples):
    verb_list = ["do", "know"]
    cnt = 0
    query_list = []
    while cnt < samples:
        randq = randint(0, 6)
        if randq <= 2:
            verb = choice(verb_list)
            query = "what are you,info\n"
            query1 = "what do you {},info\n".format(verb)
            query2 = "what can you {},info\n".format(verb)
            Qs = [query1, query2]
            query_list.append(choice(Qs))
        elif randq == 3:
            query = "who are you,info\n"
            query1 = "who made you,info\n"
            Qs = [query, query1]
            query_list.append(choice(Qs))
        elif randq == 4:
            query = "where are you,info\n"
            query_list.append(query)
        elif randq == 5:
            query = "how are you,info\n"
            query_list.append(query)
        elif randq == 6:
            query = "when were you made,info\n"
            query_list.append(query)
        cnt += 1
    return query_list

def main():

    ranked_queries = generate_rank_queries(1500)
    stat_queries = generate_stat_queries(1500)
    info_queries = generate_info_queries(1500)
    query_csv = open("data/query.csv", "a")
    for i in range(1500):
        query_csv.write(stat_queries[i])
        query_csv.write(ranked_queries[i])
        query_csv.write(info_queries[i])
    query_csv.close()
if __name__ == "__main__":
    main()
