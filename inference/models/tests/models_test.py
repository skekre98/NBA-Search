from sklearn.externals import joblib
import sys
sys.path.append("../../..")
from inference.inference_network import InferenceNetwork
import csv
import os
os.chdir('../../../')

def test_accuracy():

    model_test_map = {
        "query_classifier.py" : "inference/models/tests/test_input.csv",
    }

    for model, test_path in model_test_map.items():


        os.system('python3 ' + model) # train models, dumps into model .pkl file

        model_name = model[:len(model) - 3]

        # Query classification 
        model_file = "inference/models/classifiers/" + model_name + ".pkl"
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
    # USAGE: python3 models_test.py MODEL TESTCRITERIA
    if len(sys.argv)<2:
        print("ERROR: Missing Arguments")
        print("USAGE: python3 models_test.py MODEL TESTCRITERIA")
    elif sys.argv[1] == "classifier":
        if sys.argv[2] == "accuracy":
            test_accuracy()

models_test()
