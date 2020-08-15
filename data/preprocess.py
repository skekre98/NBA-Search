# script to preprocess data into balanced dataset 
import json
from random import choice

summary_list = []
print("Reading file")
with open("train.json") as f:
    for obj in f:
        json_summary = json.loads(obj)
        summary_list.append(json_summary)

query_list = ["Why", "why", "How", "how", "Where", "where", "Who", "who", "What", "what"]
query_csv = open("query.csv", "a")
for l in summary_list:
    for obj in l:
        line = ""
        for word in obj["summary"]:
            if word.isalpha():
                line += word + " "
            if word == ".":
                break
        query = "{} {}, 1\n".format(choice(query_list), line[:-1])
        query_csv.write(query)
query_csv.close()