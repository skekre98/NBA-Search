# NBA-Search

* This is an NBA Analytics website with multiple components such as a chatbot, blogs, and predictions. All the data for the site is being scraped from [Basketball Reference](https://www.basketball-reference.com). This project is made possible by the hard working members of the open source community!

# Usages

![image](https://user-images.githubusercontent.com/52013101/189554779-989be764-6ebe-410f-b5ae-d34b44f7f257.png)

* Live NBA Playoff Bracket section updates every game and every season so you can always stay up to date with the latest information scraped from basketball-reference.com

![image](https://user-images.githubusercontent.com/52013101/189554810-cee70883-b570-40e0-9465-8fad257df5ce.png)

* Live NBA Standings section feautures data from every game sorted by conference teams so you can always stay up to date with the latest information scraped from basketball-reference.com

![image](https://user-images.githubusercontent.com/52013101/189554827-10842dcb-5f8d-4ad1-abc1-17e23084d692.png)

* The Chatbot section can answer any questions you may have about the NBA, so you can get all your information without having to search multiple sources. Currently under development

![image](https://user-images.githubusercontent.com/52013101/189554840-1fef9d6d-a7f6-4af5-9cb2-09aed9a2a85d.png)

* The Blog section includes articles from top NBA reporters on current events scraped from basketball-reference.com. Currently under development

## System Design
![System Design](static/img/design.png)

## Building locally

1. Clone the repository locally:
   ```
   git clone https://github.com/skekre98/NBA-Search.git
   ```

2. Run the following command to set up all necessary dependencies:
   ```
   ./setup.sh
   ```
   - you will likely need to give the setup script permission to execute

3. Run the following command to deploy the web app on your localhost:
   ```
   python main.py run
   ```
<p align="center">
     <img src="/static/img/site.png">
</p>

4. Run the following command to run the unit tests:
   ```
   python main.py test
   ```
   You can also add you own unit tests in *test.py*

## Contributing

There is a lot to do so contributions are really appreciated! This is a great project for early stage developers to work with.

To begin it is recommended to start with issues labelled as [good first issue](https://github.com/skekre98/NBA-Search/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).


How to get started:

1. Fork the NBA-Search repo.
2. Create a new branch in you current repo from the 'master' branch with issue label.
3. 'Check out' the code with Git or [GitHub Desktop](https://desktop.github.com/)
4. Check [contributing.md](CONTRIBUTING.md)
5. Push commits and create a Pull Request (PR) to NBA-Search

Making a good pull request:

1. Before pushing your PR to the master branch, make sure that it builds correctly on your local machine.
2. Add enough information, like a meaningful title, the reason why you made the commit and a link to the issue page if you opened one for this PR.
3. Scope your PR to one issue. Before submitting, make sure the diff contains no unrelated changes. If you want to cover more than one issue, submit your changes for each as separate pull requests.
4. If you have added new functionality, you should update/create the relevant documentation, as well as add tests for sanity purposes.

## Dependencies
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The framework used to build the web app.
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - The HTML parser used for web scraping.
* [Sklearn](https://scikit-learn.org/stable/) - The machine learning library used to implement information retrieval.
* [Pandas](https://pandas.pydata.org/docs/) - The python library used for data manipulation.

## Troubleshooting

* Make sure you have Pip and Python installed:

```
Python3 --version
Pip3 --version
```
* If either version not found:

```
brew uninstall --ignore-dependencies python && brew install python
```

* Other Potential Errors:

```
No module named 'pandas'

pip3 install pandas   
```
```
No module named 'spacy'

pip3 install spacy
```
```
No module named 'bs4'

pip3 install beautifulsoup4
```
```
No module named 'fuzzywuzzy'

pip3 install fuzzywuzzy	
```
```
No module named 'matplotlib'

pip3 install matplotlib
```



