"""
    The crawler that fetchs the html format
    of a webstie and breaks into tags
"""
import requests
from utilities.tag import Tag
from bs4 import BeautifulSoup


class Crawler:

    # Initializing the object
    def __init__(self, urlToParse):
        self.url = urlToParse # The url that is being tracked and parsed
        self.HTML = BeautifulSoup(requests.get(urlToParse).text, 'html.parser').prettify() # The html content transfered to a string fomat

        # The writer that one writes the html format, the other one is a tester 
        self.writer = open("../logs/checks.txt", "w+")
        self.HTMLWriter = open("../logs/content.html", "w+")
        self.writeHTML(self.HTML)
        
        # Tag container
        self.tags = []

        # Traverse through the html and send the tag properties to the tags array
        self.traverse()

    # Goes through the text with a for and breaks the html 
    # into related tags with child-parent format, So the 
    # tracking would be relatively simpler
    def traverse(self):
        # Initialization
        motherTag = Tag() # The initial mother tag is basically none, because the first tag doesn't have a mother tag,
        properties = []
        tagType ,selfClosing = '', False # It's crucial to divide the tags into self closing and not self closing so the function would look for the end of the tag

        # Going through the html and identifying tags and manipulating them | Main part 
        for index in range(0, len(self.HTML)):
            # In order to avoid errors, checking for the end of the string
            if index < len(self.HTML) - 1:
                # Finding the start of the tag, avoiding the comments and end of the tags
                if self.HTML[index] == '<' and self.HTML[index + 1] != '/' and self.HTML[index] != '!':
                    # Get the values related to the tag
                    tagType, selfClosing, properties, index = self.get_tag_vals(index)

                    # if it wasn't a !DOCTYPE thing then:
                    # initialize a mother tag and name it
                    if tagType != '!DOCTYPE':
                        # Initializing a tag with the type and mother tag
                        childTag = Tag(tagType, motherTag)
                        motherTag.content.append(childTag)
                        
                        # Simple logging
                        self.write("[LOGGING]:motherTag: {}, childTag: {}".format(motherTag.describe(), childTag.describe()))

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
        self.write("[0]Tag Type: {}".format(tag_type)) # Checking the tag type identification
        index += 1 # proceed in the index

        # After exiting the first while loop, it should be checked
        # To see if the ending was because of '/' or '>'
        if self.HTML[index] == '/':
            # Self closing tag, return the with no props
            self.write("[0.5A], self-closing tag with no props, returned index: {}".format(index))
            return tag_type, props, True, index
        elif self.HTML[index] == '>':
            # Not a self-closing tag with no props
            self.write(
                "[0.5A], not a self-closing tag with no props, returned index: {}".format(index))
            return tag_type, props, selfClosing, index

        # If the function is still running the check for props begins:
        # it will get the index and they will be two kind of values,the 
        # dict type wich will be {'header': ['value1', 'value2', ...]} and the sth format
        tmp_header = '' # gets the headers
        vals = [] # gets the values for the headers
        # If a '""' was detected then it will be the second format and 
        # the data should be gotten till the end of the ""s
        notSaid = False
        # The traversing should be continued till the '/' or '>' were detected
        while self.HTML[index + 1] != '>' and self.HTML[index + 1] != '/' or self.HTML[index + 1] != '>' and self.HTML[index + 1] != '\\':
            if not notSaid :
                self.write("looking for props...")
                notSaid = True
            # Check for the start of the qoutes
            if self.HTML[index] != ' ' and self.HTML[index] != '=' and self.HTML[index] != '"':
                ("Header")
                tmp_header += self.HTML[index]
            elif self.HTML[index] == '"' and tmp_header != '':
                tmp_val = ''
                index += 1
                while self.HTML[index] != '"':
                    if (self.HTML[index] != ' ' or (self.HTML[index] == ' ' and self.HTML[index - 1] == ':')) and self.HTML[index] != ',': 
                        tmp_val += self.HTML[index]
                    else:
                        vals.append(tmp_val)
                        tmp_val= ''

                     # Goes through the string
                    if index < len(self.HTML) - 1:
                        index += 1
                    else:
                        break
                    # self.write(tmp_val)
                vals.append(tmp_val)
                # when it comes out of the loop, everything should be added
                props.append({tmp_header: vals})
                vals, tmp_header = [], '' # reset the whole thing
            
            # Goes through the string
            if index < len(self.HTML) - 1:
                index += 1
            else:
                break
            
        self.write("Props: {}".format(props))
        # After exitting the first while loop, it should be checked
        # To see if the ending was because of '/' or '>'
        if self.HTML[index] == '/':
            # Self closing tag, return the with no props
            return tag_type, props, True, index
        elif self.HTML[index] == '>':
            # Not a self-closing tag with no props
            return tag_type, props, selfClosing, index

        
        return tag_type, props, selfClosing, index
        
    # Writes to the tag
    def write(self, text):
        self.writer.write(text + "\n")

    # Writes to the tag
    def writeHTML(self, text):
        self.HTMLWriter.write(text)