# Writting tests to check the functionality of the utilities within the project
from crawler.crawl import Crawler

url = 'https://ca.finance.yahoo.com'

if __name__ == '__main__':
    crawler = Crawler(urlToParse=url)