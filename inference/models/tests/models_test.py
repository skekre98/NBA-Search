from sklearn.externals import joblib
import sys
sys.path.append("../../..")
from inference.inference_network import InferenceNetwork
import csv
import os

def test_accuracy(test_path):
    os.system('python3 query_classifier.py') # train models, dumps into query_classifier.pkl

    # Query classification 
    model_file = "../query_classifier.pkl"
    query_clf = joblib.load(model_file)


    correct = 0
    total = 0

    with open(test_path) as inputfile:
        readCSV = csv.reader(inputfile, delimiter=',')
        for row in readCSV:
            query = row[0]
            node_type = query_clf.predict([query.lower()])[0]
            total += 1
            
            if node_type.lower() == row[1].lower():
                correct += 1
            else:
                print("ON query: " + query + ", PREDICTED " + node_type.lower() + " INSTEAD OF " + row[1].lower())

    
    print("PREDICTED " + str(correct) + " OUT OF " + str(total) + ", OR " + str(correct/total) + "%")

    return "DONE"

def models_test():
    # USAGE: ./models_test MODEL TESTCRITERIA PATH_TO_TEST_CASE
    if len(sys.argv)<3:
        print("ERROR: Missing Arguments")
        print("USAGE: ./models_test MODEL TESTCRITERIA PATH_TO_TEST_CASE")
    elif sys.argv[1] == "classifier":
        if sys.argv[2] == "accuracy":
            test_accuracy(sys.argv[3])

models_test()
