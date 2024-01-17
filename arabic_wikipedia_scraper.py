# Imports
from bs4 import BeautifulSoup
import requests
import json
import os # Used only to create the output folder if it does not exist.

def get_article_soup_object(url):
    '''
    Gets a parsed object of the wikipedia page content.
    Args:
        url: String - Arabic wikipedia article URL.
    Returns:
        bs4.BeautifulSoup - A beautifulSoup object containing the parsed content of the article's page.
    '''
    url = "https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D9%86%D8%A7%D8%AF%D9%8A_%D8%A7%D9%84%D8%A3%D9%87%D9%84%D9%8A_(%D9%85%D8%B5%D8%B1)"
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def get_body_text_content(soup):
    body = soup.find(class_ = 'mw-content-rtl mw-parser-output') # Get div the contains the body of the article.
    # Remove tables and other elements to get the article's text only.
    infobox = body.find(class_ = 'infobox')
    infobox_v2 = body.find(class_ = 'infobox infobox_v2')
    navigation = body.find(class_ = 'navbox')
    hatnote = body.find(class_ = 'hatnote navigation-not-searchable')
    tables = body.find(class_ = 'wikitable')

    infobox.decompose() # Remove side info box
    infobox_v2.decompose() # Remove side info box
    navigation.decompose() # Remove navigation elements
    hatnote.decompose() # Remove hat note
    tables.decompose() # Remove tables

    return body.get_text().strip()

def get_article_list_categories(soup):
    cat_links = soup.find(id = 'mw-normal-catlinks').find_all('li') # Get div the items inside the categotiries list
    return [category_element.get_text() for category_element in cat_links ] # Iterate over all the elements in the categories list and get the element's title text.

def save_article_data_to_json(article_dict):
    file_path = 'output/{}.json'.format(article_dict['title'].replace(' ', '_'))
    os.makedirs(os.path.dirname(file_path), exist_ok=True) # If the task path is not existing it will create it.
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(article_dict, f, ensure_ascii = False, indent = 4)
        print('json file saved!')

def scrape_article(url, save_as_json = True):
    '''
    Given the article URL it scarps the article and return a dictionary containing the title, url, body text, and the categories of the article.
    If save_as_json is True it will save the dictionary's content as json file.
    Args:
        url: Srting - Arabic wikipedia article URL.
        save_as_json: Bool - wether to save to article content as json in a folder called output. Default: True.
    Returns:

    '''
    article_dict = dict()
    soup = get_article_soup_object(url)
    print('Soup object created!')
    article_dict['title'] = soup.find('h1', {'id' : 'firstHeading'}).get_text() # Get the article's title as a string.
    article_dict['url'] = url
    article_dict['body'] = get_body_text_content(soup) # Get the article's body as string.
    article_dict['categories'] = get_article_list_categories(soup)
    if(save_as_json):
        save_article_data_to_json(article_dict)
    return article_dict

# Example of how to use previous code:
#scrape_article('https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D9%86%D8%A7%D8%AF%D9%8A_%D8%A7%D9%84%D8%A3%D9%87%D9%84%D9%8A_(%D9%85%D8%B5%D8%B1)')