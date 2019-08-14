'''
    The crawler that fetchs the html format 
    of a webstie and breaks into tags
'''
import requests


class Crawler:

    def __init__(self, urlToParse):
        self.url = urlToParse
        self.HTML = requests.get(urlToParse).text
        self.writer = open("checks.txt", "w+")

    def form(self):
        for i in range(0, len(self.HTML)):
            
            # In order to avoid errors, checking for the end of the string
            if i < len(self.HTML) - 1:
                # Find the start of the tag
                if self.HTML[i] == '<' and self.HTML[i+1] != '/' and self.HTML[i+1] != '!':
                    # print("Starting Tag found...", end='')
                    tag = self.tag_type(i)
                    self.write("Starting Tag found With the tag type of: " + tag)
                    # print("With the tag type of: ", tag)

        

    """ 
        Returns the type of tag that has been detected
    """
    def tag_type(self, index):
        tmp_tag = ''

        while self.HTML[index] != ' ' and self.HTML[index] != '>' :
            if index < len(self.HTML) - 1:  
                index += 1
            else: 
                break

            tmp_tag += self.HTML[index]
            
            

        return tmp_tag

    def  write(self, text):
        self.writer.write(text + "\n")



crawler = Crawler('https://ca.finance.yahoo.com')
crawler.form()
