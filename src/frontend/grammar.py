import tatsu


class Grammar(object):
    """
    Grammar ADT for mp-compiler
    """

    def __init__(self, grammarFile='grammar.ebnf'):
        """
        Initialize grammar object
        """
        self.grammarText = str()
        self.rules = None
        try:
            with open(grammarFile, 'r') as f:
                self.grammarText = f.read()
                self.rules = tatsu.compile(self.grammarText, asmodel=True)
        except IOError:
            print("Could not read grammar file:", grammarFile)

    def __str__(self):
        """
        Print EBNF representation
        """
        return self.grammarText
