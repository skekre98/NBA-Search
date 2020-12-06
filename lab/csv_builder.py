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

import csv

from lab.visualizer import Visualizer


class CSVBuilder(Visualizer):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    # This function is to build a pie chart of the labels
    # in current csv file and load into plot
    def build_pie(self):
        labels = []
        weights = []

        with open(self.file_name, newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                if len(row) > 0:
                    label = row[len(row) - 1]

                    if label in labels:
                        weights[labels.index(label)] += 1
                    else:
                        labels.append(label)
                        weights.append(1)

        fig1, pie_chart = self.plt.subplots()
        pie_chart.pie(weights, labels=labels, autopct="%1.2f%%", startangle=90)
        pie_chart.axis("equal")
