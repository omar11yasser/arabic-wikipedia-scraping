# Wikipedia arabic articles scraping

In this project I intend to create a scraping tool for arabic wikipedia where the scraper get the paragraphs in a certain article as well as collecting all the hyperlinks for other articles inside the body and store them in a Dataframe.

The ropository enables the user to scrape a single article or a user specified number of articles by itterating over the links inside the body of the starting article and the links gathered.

The scraper will only work on Arabic Wikipedia as it has a unique structure (Diffrent from the other versions).

In a previous commit the ability to get all the article's categories listed under 'تصنيفات' was added.

Please keep in mind that the repo is not in it's final form and still under development.

## Usage
### Scraping a single article
For the ease of use the function `scrape_article` was added to `arabic_wikipedia_scraper.py` and can be used as following:
```
from arabic_wikipedia_scraper import WikipediaArabicArticleScraper

scraper = WikipediaArabicArticleScraper()
article_data = scraper.scrape_article(url, save_as_json = True) # Returns a dict or None type if the article have no title or body.
```
The `scrape_article` function's second parameter `save_as_json` defaults to true and it saves the article's data to a json file in a folder called output in the same directory the code was excuted from.

### Scraping multiple articles

```
from dataset_constructor import DatasetConstructor

dataset_maker = DatasetConstructor(url)
dataset_maker.create_dataset_from_url(number_of_articles = 500)
dataset_maker.scrape_collected_articles()
```

Make sure that the python files are in the same directory as your notebook or script.

## Future additions
In a future version I will add the ability to scrap the links I collect to create a dataset of many articles relevant to the first article I started with.
The option to get more information from the article will be added.
Further processing for the data will be added to clean the article's body.

## Warning

Please use this code responsibly and review wikepedia's rules for scrapping to check the legality and the effect of this method before usage.