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
        self.url = urlToParse # The url that is being tracked and parsed
        self.HTML = requests.get(urlToParse).text # The html content transfered to a string fomat

        # The writer that one writes the html format, the other one is a tester 
        self.writer = open("checks.txt", "w+")
        self.HTMLWriter = open("content.html", "w+")
        self.b = BeautifulSoup(self.HTML, 'html.parser').prettify()
        # self.writeHTML(self.b)
        # Tag container
        self.tags = []
        # Traverse through the html and send the tag properties to the tags array
        self.traverse()

    # Goes through the text with a for and breaks the html 
    # into related tags with child-parent format, So the 
    # tracking would be relatively simpler
    def traverse(self):
        # The initial mother tag is basically none
        # Because the first tag doesn't have a mother tag, 
        # it needs to be started at some point
        motherTag = Tag()

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
        it will go through the text where the index was given
        and it will check for the props, if the tag is self closing 
        and the type of the tag, so it will return:
            1. Tag type
            2. Props, if it has any
            3. Identify the Tag as self-closing or not
    """
    def get_tag_vals(self, index):
        # Initials variables
        tag_type = ''
        selfClosing = False
        props = []

        # Starting from the '>', we should stop 
        # when encountering a ' ' or '>' or '/'
        while (self.HTML[index + 1] != ' ' and self.HTML[index + 1] != '>' and self.HTML[index] != '/'):
            if index < len(self.HTML) - 1:
                index += 1
            else:
                break
            # Add the characters to the tag_type
            tag_type += self.HTML[index]
        
        index += 1 # proceed in the index

        # After exitting the first while loop, it should be checked 
        # To see if the ending was because of '/' or '>'
        if self.HTML[index] == '/':
            # Self closing tag, return the with no props
            return tag_type, props, True, index
        elif self.HTML[index] == '>':
            # Not a self-closing tag with no props
            return tag_type, props, selfClosing, index

        # If the function is still running the check for props begins:
        # it will get the index and they will be two kind of values,the 
        # dict type wich will be {'header': ['value1', 'value2', ...]} and the sth format
        tmp_header = '' # gets the headers
        vals = [] # gets the values for the headers
        # If a '""' was detected then it will be the second format and 
        # the data should be gotten till the end of the ""s
        
        # The traversing should be continued till the '/' or '>' were detected
        while self.HTML[index + 1] != '>' and self.HTML[index + 1] != '/' :
            # Check for the start of the qoutes
            if self.HTML[index] != ' ' and self.HTML[index] != '=' and self.HTML[index] != '"':
                tmp_header += self.HTML[index]
            elif self.HTML[index] == '"':
                tmp_val = ''
                while self.HTML[index + 1] != '"':
                    if self.HTML[index] != ' ': 
                        tmp_val += self.HTML[index]
                    else:
                        vals.append(tmp_val)
                        tmp_val= ''

                index += 1

                props.append({tmp_header: vals})
                vals, tmp_header = [], '' # reset the whole thing

        # After exitting the first while loop, it should be checked
        # To see if the ending was because of '/' or '>'
        if self.HTML[index] == '/':
            # Self closing tag, return the with no props
            return tag_type, props, True, index
        elif self.HTML[index] == '>':
            # Not a self-closing tag with no props
            return tag_type, props, selfClosing, index            


    # Writes to the tag
    def write(self, text):
        self.writer.write(text + "\n")

    # Writes to the tag
    def writeHTML(self, text):
        self.HTMLWriter.write(text)


crawler = Crawler('https://ca.finance.yahoo.com')
