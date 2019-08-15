'''
    The object that stores the information of a tag:
    1. mother tag: the tag that holds the tag within it
    2. child tag(s): the tags that might be in the tag
    - Note: a tag can both be considered as a mother and child at the same time
    3. propertis: the id/class and other values that are within a tag
    4. content: the content within a tag that incldes other child tags and text within the tag
'''

class Tag:
    
    # Defines the tag and identifies its mother tag
    def __init__(self, tagType, motherTag):

        # The mother tag of the tag, so we can track it 
        self.mother = motherTag

        # The type of the tag 
        self.type = tagType

        # An array that stores the properties of the tag such as class and id properties
        self.props = []

        # An array that stoes the content
        self.content = []

    