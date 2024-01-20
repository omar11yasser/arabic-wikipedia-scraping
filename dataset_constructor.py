# Imports
import pandas as pd

# Import useful functions from the article scrapper
from arabic_wikipedia_scraper import WikipediaArabicArticleScraper
class DatasetConstructor:
    
    def __init__(self, start_url) -> None:
        self.start_url = start_url
        self.articles_urls = list() # articles path store the path to other wikepedia articles that the current one contains.
        self.scraper = WikipediaArabicArticleScraper()
        # Add the first article to the URL links
        start_article_soup = self.scraper.get_article_soup_object(start_url)
        start_article_name = self.scraper.get_article_title_from_soup_object(start_article_soup)
        self.articles_urls.append((start_article_name, start_url))


    def check_url_validity(self, a_tag):
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

    def scrape_article_body_for_urls(self, url):
        '''
        Given the article url it gets all the URLs of the articles mentioned in the body.
        Args:
            url: String - The url of the arabic wikipedia article.
        Returns:
            articles_urls: Pandas DataFrame - Containing the articles names and URLs. The DataFrame has two columns titled name and URL.
        '''
        soup = self.scraper.get_article_soup_object(url)
        body = self.scraper.get_article_body_element(soup)
        a_tags = body.find_all('a')
        for path in a_tags:
            if self.check_url_validity(path):
                article_name = path.get('title')
                full_url = 'https://ar.wikipedia.org' + path.get('href')
                value = (article_name , full_url)
                if value not in self.articles_urls: # Check if this article exists in the list of links
                    self.articles_urls.append(value)

    def save_urls_to_csv(self):
        '''
        Saves all the obtained article urls to a csv file in the following path (From the working directory): output/obtained_links.csv.
        '''
        urls_df = pd.DataFrame.from_records(self.articles_urls, columns= ['name', 'URL'])
        urls_df.to_csv('output/obtained_links.csv', index= False)
        print('Numbers of urls in the csv file: ', urls_df.shape[0])

    def create_dataset_from_url(self, number_of_articles = 5000):
        '''
        Start gathering links from the article passed while creating the object.
        Then itterate over all the articles gathered until it exceeds the number of articles specified by the user.
        Args:
        numebr of articles: The number of articles urls the user want to gather (Aproximetly).
        '''
        counter = 0
        while len(self.articles_urls) < number_of_articles:
            self.scrape_article_body_for_urls(self.articles_urls[counter][1])
            counter += 1
        print('Articles URLs collected: ', len(self.articles_urls))

    def scrape_collected_articles(self):
        '''
        Srape all the collected articles and save them as json objects.
        Should be called after create_dataset_from_url.
        '''
        for article in self.articles_urls:
            self.scraper.scrape_article(article[1], True)
