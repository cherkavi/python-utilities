# SPHINX Walkthrough

This is a walkthrough of the SPHINX workflow. It is intended to be a quick reference guide. The python work used in this repository is based on a different repository and the credits for the code go to the original authors. The original repository can be found [here](https://github.com/cherkavi/python-utilities)

## Setup

1. The workflow is divided into 3 steps:

```bash

# Preprocessing: Generate markdown files from the original scripts
bash scripts/generate_markdown.sh doc/pages
```

2. To embed the code into markdown files, run the following command:

```bash
# TODO: Add the command to embed the code
```

3. To setup sphinx, run the following commands:

```bash
python3 -m pip install -U sphinx sphinx_rtd_theme myst-parser
cd doc
make html
```
