from tatsu.codegen import ModelRenderer
from tatsu.codegen import CodeGenerator

import sys

THIS_MODULE = sys.modules[__name__]


class PythonGenerator(CodeGenerator):
    """
    Code generation backend
    """

    def __init__(self):
        super().__init__(modules=[THIS_MODULE])

    @classmethod
    def format(self, code):
        """
        save code
        """
        with open("example/conversation.py",
                  'w',
                  encoding='utf-8',
                  newline='') as f:
            f.write(code)


"""
Renderer templates
"""

CODE_TEMPLATE = """\
\"\"\"
# -*- coding: UTF-8 -*-
Conversation module for Agent [AGENT_NAME]

Specification: LINK_TO_SPECIFICATION

@author: [AUTHOR]
@email: [EMAIL]
\"\"\"

from .conversation import Conversation

# rename this class to "[AGENT_NAME]Conversation"


class templateConversation(Conversation):
    \"\"\"Conversation logic for [AGENT_NAME]
    \"\"\"

    def __init__(self, username, userId, agent, cnHelper=None, enHelper=None, gameProgress=None, actionHandler=None):
        \"\"\"Setup private variables & call parent constructor
        \"\"\"
        super().__init__(username, userId, agent, 
                            cnHelper=cnHelper, enHelper=enHelper, 
                            gameProgress=gameProgress, actionHandler=actionHandler)
        
        # stack of intents to manage context
        self._intents = []

        pass

    def _generateResponseText(self, intent, entities, difficulty):
        \"\"\"
        Generate response according to received intent
        \"\"\"
        text = ""

        if intent in ['positive', 'negative']:
            if len(self._intents) > 0:
                stacked = self._intents.pop()
                text = self._randomResponse(
                    '-'.join([stacked, intent]), difficulty)

        {sectionList::\n\t\t:%s}

        return text

    def takeActions(self, userInput, agentResponse, debugInfo, gameProgressProfile):
        \"\"\"
        Other actions than text response
        \"\"\"
        super().takeActions(userInput, agentResponse, debugInfo, gameProgressProfile)

        pass
"""


class Dialog(ModelRenderer):
    """
    Dialog renderer
    """
    template = CODE_TEMPLATE


class Intent(ModelRenderer):
    template = "{intentID}"


class ID(ModelRenderer):
    template = "{IDString}"


class Section(ModelRenderer):
    def render_fields(self, fields):
        if fields["subSectionList"]:
            self.template = '''\
            if intent == "{intent}": text += self._randomResponse(intent, difficulty) ; self._intents.append(intent)    
            '''
        else:
            self.template = '''\
            if intent == "{intent}": text += self._randomResponse(intent, difficulty)
            '''
