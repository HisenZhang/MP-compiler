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

    def __init__(self, username, userId, gesture_handler, agent, cnHelper=None, enHelper=None, gameProgress=None):
        \"\"\"Setup private variables & call parent constructor
        \"\"\"
        super().__init__(username, userId, gesture_handler,
                         agent, cnHelper, enHelper, gameProgress)

    def _generateResponseText(self, intent, entities, difficulty):
        \"\"\"
        Generate response according to received intent
        \"\"\"
        text = ""

        {sectionList::\n\t\t:%s}

        return text

    def takeActions(self, userInput, agentResponse, debugInfo, gameProgressProfile):
        \"\"\"
        Other actions than text response
        \"\"\"
        super().takeActions(userInput, agentResponse, debugInfo, gameProgressProfile)

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
    template = '''\
    if intent == "{intent}": text += self._randomResponse(intent, difficulty)    
    '''
