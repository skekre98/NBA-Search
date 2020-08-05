<p align="center">
     <img src="/static/img/AI-Orange.png" width="600" height="400">
</p> 

# NBA-Search

This is an NBA Analytics website with multiple components such as a chatbot, blogs, and predictions. All the data for the site is being scraped from [Basketball Reference](https://www.basketball-reference.com).

## Building locally

1. Clone the repository locally:
   ```
   git clone https://github.com/skekre98/NBA-Search.git
   ```

2. Run the following command to set up all necessary requirements:
   ```
   pip install -r requirements.txt
   ```

3. Run the following command to deploy the web app on your localhost:
   ```
   python main.py run
   ```

4. Run the following command to run the unit tests:
   ```
   python main.py test
   ```
   You can also add you own unit tests in *test.py*

## Dependencies
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The framework used to build the web app.
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - The HTML parser used for web scraping.
* [Sklearn](https://scikit-learn.org/stable/) - The machine learning library used to implement information retrieval.
* [Pandas](https://pandas.pydata.org/docs/) - A python library used for data manipulation.