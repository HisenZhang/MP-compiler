
import tatsu
import sys
from backend.pythonGenerator import PythonGenerator
from backend.policyGenerator import PolicyGenerator

grammar = open('grammar.ebnf').read()
source = str()

if len(sys.argv) == 1:
    source = sys.stdin.read()
else:
    source = open(sys.argv[1], 'r', encoding='utf-8').read()

parser = tatsu.compile(grammar, asmodel=True)
model = parser.parse(source)

# ast = tatsu.util.asjson(tatsu.compile(grammar).parse(TEST_STRING))
# print(json.dumps(ast, indent=2))

print('# TRANSLATED TO python')
code = PythonGenerator().render(model)
PythonGenerator.format(code)
print(code)


record = PolicyGenerator().render(model)
print(record)
policy, csv = PolicyGenerator.format(record)
print('# POLICY')
print(policy)
print('# CSV')
print(csv)
