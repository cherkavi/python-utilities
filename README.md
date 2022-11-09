# SPHINX Walkthrough

This is a walkthrough of the SPHINX workflow. It is intended to be a quick reference guide. The python work used in this repository is based on a different repository and the credits for the code go to the original authors. The original repository can be found [here](https://github.com/cherkavi/python-utilities)

## Setup

1. The workflow is divided into 3 steps:

```bash

# Preprocessing: Generate markdown files from the original scripts
# In root directory,
bash scripts/generate_markdown.sh doc/pages
```

2. To embed the code into markdown files, run the following command:

```bash
# TODO: Add the command to embed the code
```

3. To setup sphinx, run the following commands:

```bash
# In Ubuntu 20.04
sudo apt-get install texlive texlive-latex-extra pandoc
python3 -m pip install -r requirements.txt
cd doc
make html
```
