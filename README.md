# Wikipedia arabic articles scraping

In this project I intend to create a scraping tool for arabic wikipedia where the scraper get the paragraphs in a certain article as well as collecting all the hyperlinks for other articles inside the body and store them in a Dataframe.

The scraper will only work on Arabic Wikipedia as it have a unique structure.

In a previous commit the ability to get all the article's categories listed under 'تصنيفات' was added.

Please keep in mind that the repo is not in it's final form and still under development.

## Usage
For the ease of use the function `scrape_article` was added to `arabic_wikipedia_scraper.py` and can be used as following:
```
from arabic_wikipedia_scraper import scrape_article

article_data = scrape_article(url, save_as_json = True)
```
The `scrape_article` function's second parameter `save_as_json` defaults to true and it saves the article's data to a json file in a folder called output in the same directory the code was excuted from.
Make sure that the python file is in the same directory your are working from.

The function also can be used from the bottom of the python file `arabic_wikipedia_scraper.py`.

## Future additions
In a future version I will add the ability to scrap the links I collect to create a dataset of many articles relevant to the first article I started with.
The option to get more information from the article will be added.
Further processing for the data will be added to clean the article's body.

## Warning

Please use this code responsibly and review wikepedia's rules for scrapping to check the legality and the effect of this method before usage.