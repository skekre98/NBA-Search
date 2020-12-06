# Copyright (c) 2020 Sharvil Kekre skekre98
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

    if len(sys.argv) <= 1:
        print("ERROR: Missing Arguments")
        printHelp()
    elif sys.argv[1] == "test":
        print("Flask Tests")
        os.system("python3 -W ignore -m unittest tests/flask_tests.py")
        print("Module Tests")
        os.system("python3 -W ignore -m unittest tests/module_tests.py")
        print("Inference Tests")
        os.system("python3 -W ignore -m unittest tests/inference_tests.py")
    elif sys.argv[1] == "run":
        os.system("python3 app.py")
    elif sys.argv[1] == "data":
        os.system("python3 visualize.py")
    else:
        print("ERROR: Invalid Arguments")
        printHelp()


if __name__ == "__main__":
    main()
