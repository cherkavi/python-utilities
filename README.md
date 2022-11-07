# SPHINX Walkthrough

This is a walkthrough of the SPHINX workflow. It is intended to be a quick reference guide. The python work used in this repository is based on a different repository and the credits for the code go to the original authors. The original repository can be found [here](https://github.com/cherkavi/python-utilities)

## Setup

The workflow is divided into 3 steps:

```bash

# Preprocessing: Generate markdown files from the original scripts
bash scripts/generate_markdown.sh doc/pages
```

To setup sphinx, run the following commands:

```bash
python3 -m pip install -- sphinx sphinx_rtd_theme
cd doc
make html
```
