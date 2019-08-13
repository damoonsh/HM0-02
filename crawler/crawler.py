'''
    The crawler that fetchs the html format of a webstie
    and breaks into tags
'''
import requests


class Crawler:
    def __init__(self, urlToParse):
        self.url = urlToParse