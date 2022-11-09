# This is a sample Python script.
import os
from jinja2 import Environment, FileSystemLoader, Template


def make_from_file() -> str:
    env = Environment(loader=FileSystemLoader(os.path.dirname(".")))
    template = env.get_template(os.path.basename("message-template.j2"))
    return template.render(URL='my replace text for file')

def make_from_text() -> str:
    with open('message-template.j2') as f:
        lines = f.readlines()
        template = Template("".join(lines))
        return template.render(URL='my replace text')


if __name__ == '__main__':
    print(make_from_file())
    print("-----------------")
    print(make_from_text())
