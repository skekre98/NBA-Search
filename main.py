import os
import sys

# Function to print help message
def printHelp():
    print("usage: python main.py {test | run}")
    print("  options:")
    print("    test: runs unit tests for backend functions")
    print("    run: Runs Flask server on localhost port 5000")
    print("    data: data visualization for training sets")

def main():

    # Removing training history inside sqlite3 file 
    try:
        print("Removing previous training instance")
        os.remove('db.sqlite3')
    except OSError:
        print("No previous instance detected")

    if len(sys.argv)<=1:
        print("ERROR: Missing Arguments")
        printHelp()
    elif sys.argv[1] == "test":
        os.system('python3 -m unittest test.py')
    elif sys.argv[1] == "run":
        os.system('python3 app.py')
    elif sys.argv[1] == "data":
        os.system('python3 visualize.py')
    else:
        print("ERROR: Incorrect Arguments")
        printHelp()


if __name__ == "__main__":
    main()