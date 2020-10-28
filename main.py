import os
import sys

# Function to print help messages
def printHelp():
    print("usage: python main.py {test, run, data, train}")
    print("  options:")
    print("    test: runs unit tests for backend functions")
    print("    run: Runs Flask server on localhost port 5000")
    print("    data: data visualization for training sets")
    print("    train: trains a new query classification model")

def main():

    # Removing training history inside sqlite3 file 
    
    if len(sys.argv)<=1:
        print("ERROR: Missing Arguments")
        printHelp()
    elif sys.argv[1] == "test":
        os.system('python3 -m unittest test.py')
    elif sys.argv[1] == "run":
        os.system('python3 app.py')
    elif sys.argv[1] == "data":
        os.system('python3 visualize.py')
    elif sys.argv[1] == "train":
        os.system('python3 query_classifier.py')
    else:
        print("ERROR: Invalid Arguments")
        printHelp()


if __name__ == "__main__":
    main()
