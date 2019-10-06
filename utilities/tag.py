"""
    The object that stores the information of a tag:
    1. mother tag: the tag that holds the tag within it
    2. child tag(s): the tags that are in the tag
    - Note: a tag can both be considered as a mother and child at the same time, it is relative
    3. properties: the id/class and other values that are within a tag
    4. content: the content within a tag that includes other child tags and text within the tags
"""


class Tag:

    # Defines the tag and identifies its mother tag
    def __init__(self, tagType='', motherTag='', self_closing=False):
        # The mother tag of the tag, so we can track it
        self.mother = motherTag

        # The type of the tag 
        self.type = tagType

        # An array that stores the properties of the tag such as class and id properties
        self.props = []

        # An array that stores the content
        self.content = []

        # A boolean that shows if the tag is self-closing or not
        self.selfClosing = self_closing

    # Describes the properties of the tag, just for checking and logging (no actual usage)
    def describe(self):
        # There is a tag with no mom that needs to be considered otherwise a error will be given
        if self.mother  == '':
            return ("Tag Type: {}, mother:{}, props:{}, content:{}, self-closing:{}".format(self.type, 'no mother tag', self.props, self.content, self.selfClosing))
        # Return the default version where a mother tag exists.
        return ("Tag Type: {}, mother:{}, props:{}, content:{}, self-closing:{}".format(self.type, self.mother.type, self.props, self.content, self.selfClosing))