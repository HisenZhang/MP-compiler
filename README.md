# MP-compiler

Turning human readable dialogue script into machine executable code.

Check out detailed project page on [Notion](https://www.notion.so/MP-Compiler-c9771abfb5744d7a9e94db6556209c20).

## Input

The sample input file is `example/test.dlg`. Make it the first argument for main.py, or the program will read from `stdin`. When finished, end your input with EOF.

## Output

At this moment the generated files require manual integration to the dialog engine.

- intent.csv: Upload to Watson
- policy.json: Append to the existing policy
- conversation.py: Copy to the dialog directory
