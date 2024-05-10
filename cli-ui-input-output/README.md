# cli user interface

[my own examples of console UI application](https://github.com/cherkavi/networking-reminder/tree/main/)

## prompt_toolkit
```py
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

while 1:
    user_input = prompt('>', 
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                       )
    print(user_input)
```
```python
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter

SQLCompleter = WordCompleter(['select', 'from', 'insert', 'update', 'delete', 'drop'],
                             ignore_case=True)

while 1:
    user_input = prompt('SQL>', 
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=SQLCompleter,
                        )
    print(user_input)
```

## Click
```sh
pip install click
```
```python
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
import click

SQLCompleter = WordCompleter(['select', 'from', 'insert', 'update', 'delete', 'drop'],
                             ignore_case=True)

while 1:
    user_input = prompt(u'SQL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=SQLCompleter,
                        )
    click.echo_via_pager(user_input)
```

```py
import click
message = click.edit()
```

```py
import click


@click.group()
def main():
    pass


@main.command()
@click.option("--a", prompt=" Enter the first number", type=int)
@click.option("--b", prompt=" Enter the second number", type=int)
def add(a, b):
    value = a + b
    click.echo(" The added value {}".format(value))


@main.command()
@click.option("--a", prompt=" Enter the first number", type=int)
@click.option("--b", prompt=" Enter the second number", type=int)
def sub(a, b):
    value = a - b
    click.echo(" The difference is {}".format(value))


@main.command()
@click.option("--a", prompt=" Enter the first number", type=int)
@click.option("--b", prompt=" Enter the second number", type=int)
def mul(a, b):
    value = a * b
    click.echo(" The multiplied value {}".format(value))


@main.command()
@click.option("--a", prompt=" Enter the first number", type=int)
@click.option("--b", prompt=" Enter the second number", type=int)
def div(a, b):
    value = a / b
    click.echo(" The  value {}".format(value))


if __name__ == "__main__":
    main()

```

## fuzzy finder
```sh
pip install fuzzyfinder
```
```py
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
import click
from fuzzyfinder import fuzzyfinder

SQLKeywords = ['select', 'from', 'insert', 'update', 'delete', 'drop']

class SQLCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, SQLKeywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))

while 1:
    user_input = prompt(u'SQL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=SQLCompleter(),
                        )
    click.echo_via_pager(user_input)
```

## pygments
```sh
pip install pygments
```
```py
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
import click
from fuzzyfinder import fuzzyfinder
from pygments.lexers.sql import SqlLexer

SQLKeywords = ['select', 'from', 'insert', 'update', 'delete', 'drop']

class SQLCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, SQLKeywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))

while 1:
    user_input = prompt(u'SQL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=SQLCompleter(),
                        lexer=SqlLexer,
                        )
    click.echo_via_pager(user_input)
```

## [PyInquirer](https://github.com/CITGuru/PyInquirer)
[examples](https://github.com/CITGuru/PyInquirer?tab=readme-ov-file#examples)  
```py
from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


questions = [
    {
        'type': 'checkbox',
        'message': 'Select toppings',
        'name': 'toppings',
        'choices': [
            Separator('= The Meats ='),
            {
                'name': 'Ham'
            },
            {
                'name': 'Ground Meat'
            },
            {
                'name': 'Bacon'
            },
            Separator('= The Cheeses ='),
            {
                'name': 'Mozzarella',
                'checked': True
            },
            {
                'name': 'Cheddar'
            },
            {
                'name': 'Parmesan'
            },
            Separator('= The usual ='),
            {
                'name': 'Mushroom'
            },
            {
                'name': 'Tomato'
            },
            {
                'name': 'Pepperoni'
            },
            Separator('= The extras ='),
            {
                'name': 'Pineapple'
            },
            {
                'name': 'Olives',
                'disabled': 'out of stock'
            },
            {
                'name': 'Extra cheese'
            }
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]

answers = prompt(questions, style=style)
pprint(answers)
```

```py
from PyInquirer import prompt
from examples import custom_style_2
from prompt_toolkit.validation import Validator, ValidationError


class NumberValidator(Validator):

    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))




questions = [
    {
        'type': 'list',
        'name': 'user_option',
        'message': 'Welcome to simple calculator',
        'choices': ["sum","difference","product", "divide"]
    },

    {
        'type': "input",
        "name": "a",
        "message": "Enter the first number",
        "validate": NumberValidator,
        "filter": lambda val: int(val)
    },

    {
        'type': "input",
        "name": "b",
        "message": "Enter the second number",
        "validate": NumberValidator,
        "filter": lambda val: int(val)
    }


]

def add(a, b):
    print(a + b)

def difference(a, b):
    print(a - b)

def product(a, b):
    print(a * b)


def divide(a, b):
    print(a / b)


def main():
    answers = prompt(questions, style=custom_style_2)
    a = answers.get("a")
    b = answers.get("b")
    if answers.get("user_option") == "sum":
        add(a, b)
    elif answers.get("user_option") == "difference":
        difference(a, b)
    elif answers.get("user_option") == "product":
        product(a, b)
    elif answers.get("user_option") == "divide":
        divide(a, b)


if __name__ == "__main__":
    main()
```

## [cliff](https://docs.openstack.org/cliff/latest/)
for building interactive applications

## other relative frameworks
* https://github.com/open-iscsi/configshell-fb/tree/master
* Docopt

