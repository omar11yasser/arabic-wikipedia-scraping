# Imports
import pandas as pd

# Import useful functions from the article scrapper
from arabic_wikipedia_scraper import get_article_soup_object
from arabic_wikipedia_scraper import get_article_body_element

def check_url_validity(a_tag):
    '''
    Given an a tag which contains the title and the path of the article, this function decides whether it should be added as part of the dataset or note.
    Args: 
        a_tag: bs4.element.Tag - a tag extracted from the body of the article.
    Returns:
        Boolean: True if the url will be added to the dataset.
    '''
    article_name = a_tag.get('title')
    article_path = a_tag.get('href')
    try:
        if article_name == None or article_path == None or 'توضيح' in article_name or 'png' in article_path or 'www.' in article_path:
            return False
        if a_tag.get('class') == None and 'cite_note' not in article_path:
            return True
    except KeyError:
        print('Key error has occured!')
        return False


def get_article_body_links(body):
    '''
    Given the article body soup object it gets all the URLs of the articles mentioned in the body.
    Args:
        body: bs4.element.Tag - The content of the body elemenet of the article.
    Returns:
        articles_urls: Pandas DataFrame - Containing the articles names and URLs. The DataFrame has two columns titled name and URL.
    '''
    a_tags = body.find_all('a')
    articles_path = list() # articles path store the path to other wikepedia articles that the current one contains
    print('Number of a tags:', len(a_tags))
    for path in a_tags:
        if check_url_validity(path):
            article_name = path.get('title')
            full_url = 'https://ar.wikipedia.org' + path.get('href')
            value = (article_name , full_url)
            if value not in articles_path: # Check if this article exists in the list of links
                articles_path.append(value)

    return pd.DataFrame.from_records(articles_path, columns= ['name', 'URL'])

def create_dataset(url, number_of_articles = 5000):
    soup = get_article_soup_object(url)
    print('Soup object created!')
    body = get_article_body_element(soup)
    links_df = get_article_body_links(body)
    print('Numbers of urls in the output dataframe: ', links_df.shape[0])
    links_df.to_csv('output/obtained_links.csv', index= False)

# Usage example 
#create_dataset('https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D9%86%D8%A7%D8%AF%D9%8A_%D8%A7%D9%84%D8%A3%D9%87%D9%84%D9%8A_(%D9%85%D8%B5%D8%B1)')