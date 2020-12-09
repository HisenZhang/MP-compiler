from tatsu.codegen import ModelRenderer
from tatsu.codegen import CodeGenerator

import json
import csv

import sys
from collections import OrderedDict

THIS_MODULE = sys.modules[__name__]


class PolicyGenerator(CodeGenerator):
    """
    policy.json generation backend
    """

    def __init__(self):
        super().__init__(modules=[THIS_MODULE])

    @classmethod
    def format(cls, record):
        """Format the parsed intermediate record into JSON and CSV

        Args:
            record (Record): The rendered intermediate structure

        Returns:
            (str,str): strings of JSON and CSV representation

        """
        csvfile = open('example/intent.csv', 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)

        jsonfile = open('example/policy.json', 'w')

        example_csv = list()
        lines = record.splitlines()
        outer = dict()

        # For tones to concatnate.
        last_intent = ''

        def splitCN(CNString):
            """
            Split CN string word by word
            """
            return ' '.join(CNString)

        for l in lines:
            if l.strip() == '':
                continue
            ctx = l.split('^^^')
            for c in ctx:
                stmt = c.split(':')
                intent, trigger, agent = stmt[0].split('...')
                trigger = trigger[1:-1]

                if intent[0] == '@':
                    intent = last_intent + '-' + intent[1:]
                else:
                    last_intent = intent

                for item in [s.split('///')
                             for s in trigger.split('|||')]:

                    if len(item) > 1:
                        example_csv.append((item[0], intent))
                        example_csv.append((splitCN(item[1]), intent))
                        csv_writer.writerow([item[0], intent])
                        csv_writer.writerow([splitCN(item[1]), intent])

                    else:
                        example_csv.append((item[0], intent))
                        csv_writer.writerow([item[0], intent])

                if agent not in outer.keys():
                    outer[agent] = dict()
                if intent not in outer[agent].keys():
                    outer[agent][intent] = list()
                outer[agent][intent] = [s.split('///')
                                        for s in stmt[1].split('|||')]

        def nextIntent():
            for agent in outer:
                for intent in outer[agent]:
                    intentList = list()
                    for stmt in outer[agent][intent]:

                        # if stmt dose not have CN, take the value of the default one (EN)
                        en = stmt[0]
                        if len(stmt) > 1:  # more than one alt statement available
                            cn = stmt[1]
                        else:
                            cn = stmt[0]

                        # decide the type of statement.
                        #
                        # 'question' if ended with question mark
                        # else 'answer'
                        t = 'question' if cn[-1] == '？' or en[-1] == '?' else 'answer'

                        metadata = dict()

                        metadata["CN"] = cn
                        metadata["EN"] = en
                        metadata["difficulty"] = 1
                        metadata["type"] = t
                        metadata["format"] = "text"
                        metadata["slot"] = ""
                        metadata["auto_fill"] = []
                        metadata["uuid"] = ""
                        metadata["jump_to_intent"] = ""

                        intentList.append(metadata)

                    yield {intent: intentList}

        def nextAction():
            for agent in outer:
                intents = {}
                for i in nextIntent():
                    intents.update(i)

                # "action" is the default key
                yield {"action": intents}

        def nextAgent():
            for agent in outer:
                for i in nextAction():
                    yield {agent: i}

        policy = dict()
        [policy.update(p) for p in nextAgent()]
        policy_json = json.dumps(policy, indent=2)

        jsonfile.write(policy_json)

        # TODO fix CSV output for example intents
        intent_csv = example_csv

        csvfile.close()
        jsonfile.close()

        return (policy_json, intent_csv)


"""
Renderer templates
"""


class Dialog(ModelRenderer):
    template = "{sectionList::\n:}"


class Section(ModelRenderer):
    template = "{statementList:::{intent}...({trigger})...%s\n}{subSectionList:::}"


class EquivalentStatement(ModelRenderer):
    template = "{stmt::/:}"


class AlternativeStatement(ModelRenderer):
    template = "{stmt::|:}"


class Statement(ModelRenderer):
    template = "{agent}:{content}"


class ID(ModelRenderer):
    template = "{IDString}"


class Agent(ModelRenderer):
    template = "{agentID}"


class Intent(ModelRenderer):
    template = "{intentID}"


class Tone(ModelRenderer):
    template = "^^^{statementList::^^^:@{toneID}...({trigger})...%s}"
