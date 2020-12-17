# -*- coding: utf-8 -*-
import tatsu
import json
import pprint

from config import config


class Parser(object):
    """
    Parser from MP-compiler
    """

    def __init__(self, rules: tatsu.grammars.Grammar):
        """Create parser object

        Args:
            grammar (tatsu.grammars.Grammar): grammar rules
        """
        self.rules = rules
        self.ast = None
        pass

    def parse(self, source: str) -> tatsu.ast.AST:
        """Parse from Source

        Args:
            source (str): Text input 

        Returns:
            tatsu.ast.AST: The parsed AST
        """
        self.ast = tatsu.parse(self.rules, source,
                               trace=config['DEBUG'], colorize=config['DEBUG'])
        self.json = tatsu.util.asjson(self.ast)
        return self.ast

    def printAST(self, format='JSON'):
        """Pretty print the AST object

        Args:
            format (str, optional): Format to print AST. Defaults to 'JSON'.
        """
        if format == 'JSON':
            print(json.dumps(self.json, indent=2))
        elif format == 'PPRINT':
            pprint(ast, width=20, indent=4)
