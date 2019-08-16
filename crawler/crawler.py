"""
    The crawler that fetchs the html format
    of a webstie and breaks into tags
"""
import requests
from tag import Tag
from bs4 import BeautifulSoup


class Crawler:

    # Initializing the object
    def __init__(self, urlToParse):
        self.url = urlToParse
        self.HTML = requests.get(urlToParse).text
        self.writer = open("checks.txt", "w+")
        # self.HTMLWriter = open("content.html", "w+")
        # self.b = BeautifulSoup(self.HTML, 'html.parser').prettify()
        # self.writeHTML(self.b)
        self.tags = []
        self.traverse()

    # Goes through the text with a for and breaks the html 
    # into related tags with child-parent format, So the 
    # tracking would be relatively simple
    def traverse(self):
        # The initial mother tag is basically none
        # Because the first tag didn't hav a mother tag
        motherTag = Tag()
        selfClosing, haveProps = False, False

        # Going through the html and identifying tags and manipulating them
        for index in range(0, len(self.HTML)):
            # In order to avoid errors, checking for the end of the string
            if index < len(self.HTML) - 1:
                # Find the start of the tag
                # Avoiding the comments and end of the tags
                if self.HTML[index] == '<' and self.HTML[index + 1] != '/' and self.HTML[index + 1] != '!':
                    # Get the type of tag that is encountered
                    index, tagType, selfClosing, haveProps = self.tag_type(index)
                    
                    # Get the props of the tag
                    if haveProps:
                        get_props()

                    # if it wasn't a !DOCTYPE thing then:
                    # initialize a mother tag and name it
                    if tagType != '!DOCTYPE':
                        # Initializing a tag with the type and mother tag
                        childTag = Tag(tagType, motherTag)
                        motherTag.content.append(childTag)

                        # Simple logging
                        self.write("type: {}, selfClosing: {}, mother: {}".format(tagType, selfClosing, childTag.mother.type))
                        motherTag = childTag

                # if we have reached to the end of the tag that means 
                # the mother and child should be resetted
                if self.HTML[index] == '<' and self.HTML[index + 1] == '/':
                    # If the mother tag had a mother tag then switch the mother tags
                    if childTag.mother != '':
                        motherTag = childTag.mother
                    self.write("End of the tag, going to back to {}".format(motherTag.type))

    """ 
        1. Returns the type of tag that has been detected
        Note: It is crucial to identify if the tag is self-closing or not
    """
    def tag_type(self, index):
        # The while loop that identifies the type of the tag
        tmp_tag = ''  # The temporary container that gets the tag type
        self_closing = False

        while self.HTML[index + 1] != ' ' and self.HTML[index + 1] != '>' and self.HTML[index] != '/':
            if index < len(self.HTML) - 1:
                index += 1
            else:
                break

            tmp_tag += self.HTML[index]

        self_closing = self.if_selfClosing(index)
        
        if self.HTML[index + 1] == ' ':
            prop = True
        else: 
            prop = False

        return index, tmp_tag, self_closing, prop

    # Checks if the tag is self-closing or not
    def if_selfClosing(self, index):
        # Whil not reached to the end of the tag
        while self.HTML[index] != '>':
            if index < len(self.HTML) - 1:
                index += 1
            else:
                break

        if self.HTML[index - 1] == '/':
            return True

        return False

    
    """ 
        2. Gets the props of the tag:
            - it will get the index and they will be two kind of values,
            the dict type wich will be {'header': ['value1', 'value2' ,...]} and the sth format
    """
    def get_props(self,index):
        # The props of the tag
        tmp_header = ''
        tmp_val = []
        tmp_props = [] # Keeps the data about the tag properties

        # A variable that identifies if it had reached a '=' or not
        equals = False

        # Since we are within the tag, then the end of it would be '>'
        while self.HTML[index + 1] != '>' or self.HTML[index + 1] != '/':
            # If encountered a '=', then we are in the dict format
            if self.HTML[index] == '=':
                index += 1 # So, proceed through the text and don't get the '='
                equals = True

            # if it was anything but ' ' then save it
            if self.HTML[index] != ' ' and not equals: # Get into header
                tmp_header += self.HTML[index]
            elif self.HTML[index] != ' ' and equals: # Get into value
                tmp_val += self.HTML[index]

            # If it was ' ', then append to the props
            if self.HTML[index] == ' ':
                equals = False # resetting the equals to False again
                if tmp_val != '': # Form of dict
                    tmp_props.append({tmp_header: tmp_val})
                else: # Form of no-dict
                    tmp_props.append(tmp_header)            
            
            # Prevent the erros
            if index < len(self.HTML) - 1:
                index += 1
            else:
                break


    # Writes to the tag
    def write(self, text):
        self.writer.write(text + "\n")

    # Writes to the tag
    def writeHTML(self, text):
        self.HTMLWriter.write(text)


crawler = Crawler('https://ca.finance.yahoo.com')
