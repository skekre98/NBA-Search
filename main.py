import os
import sys
import unittest
import tests.flask_tests as flask_tests
import tests.module_tests as module_tests
import tests.inference_tests as inference_tests
from app import app as application
import visualize

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
        suite = unittest.TestLoader().loadTestsFromModule(flask_tests)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print("Module Tests")
        suite = unittest.TestLoader().loadTestsFromModule(module_tests)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print("Inference Tests")
        suite = unittest.TestLoader().loadTestsFromModule(inference_tests)
        unittest.TextTestRunner(verbosity=0).run(suite)
    elif sys.argv[1] == "run":
        application.run()
    elif sys.argv[1] == "data":
        visualize.main()
    else:
        print("ERROR: Invalid Arguments")
        printHelp()


if __name__ == "__main__":
    main()
