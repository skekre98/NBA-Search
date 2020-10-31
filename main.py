import os
import sys

# Function to print help messages
def printHelp():
    print("usage: python main.py {test, run, data}")
    print("  options:")
    print("    test: runs unit tests for backend functions")
    print("    run: Runs Flask server on localhost port 5000")
    print("    data: data visualization for training sets")

def main():
    
    if len(sys.argv)<=1:
        print("ERROR: Missing Arguments")
        printHelp()
    elif sys.argv[1] == "test":
        print("Flask Tests")
        os.system('python3 -W ignore -m unittest tests/flask_tests.py')
        print("Module Tests")
        os.system('python3 -W ignore -m unittest tests/module_tests.py')
        print("Inference Tests")
        os.system('python3 -W ignore -m unittest tests/inference_tests.py')
    elif sys.argv[1] == "run":
        os.system('python3 app.py')
    elif sys.argv[1] == "data":
        os.system('python3 visualize.py')
    else:
        print("ERROR: Invalid Arguments")
        printHelp()


if __name__ == "__main__":
    main()
