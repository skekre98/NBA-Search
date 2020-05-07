import os
import sys

# Function to print help message
def printHelp():
    print("usage: python main.py {test | run}")
    print("  options:")
    print("    test: runs unit tests for backend functions")
    print("    run: Runs Flask server on localhost port 5000")

def main():
    if len(sys.argv)<=1:
        print("ERROR: Missing Arguments")
        printHelp()
    elif sys.argv[1] == "test":
        os.system('python -m unittest test.py')
    elif sys.argv[1] == "run":
        os.system('python app.py')
    else:
        print("ERROR: Incorrect Arguments")
        printHelp()


if __name__ == "__main__":
    main()