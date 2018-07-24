# Genealogy Model 3

This is the third version of my simple genealogy modeler. This program creates randomized genealogies with a process influenced by several customizable parameters.

## The `makegen` tool

This tool allows easy customized running of genealogy examinations. The kinds of runs implemented so far are:

- Single Genealogy
- Single-Trait

### Dependencies

Make sure your have the following installed:

- [python3](https://www.python.org/download/releases/3.0/)
- [Graphviz](https://www.graphviz.org/) (free download)
- Various python packages listed in `requirements.txt`. These can be installed with `pip install -r requirements.txt`

### Downloading

Before running anything, you will need to download this repository. I suggest doing something like the following in terminal (command line):

    $ cd ~/Documents/
    $ git clone https://github.com/Riib11/GenealogyModel3.git

This will create a directory named `GenealogyModel3/` in your main documents directory (`~/Document`). To use this method, you will need to have [`git`](https://git-scm.com/download/mac) installed

### Running `makegen`

1. Create a new file `<config-name>.json` in the `makegen_configs/` directory, where `<config-name>` is the name of this config file.
2. Customize the settings in the json file, following the template of `template.json`.
3. Open terminal (command line) and execute the following:

```
    $ cd /path/to/GenealogyModel3/
    $ python3 makegen.py makegen_config/<config-name>.json
```

The first line navigates to the GenealogyModel3 directory (wherever it happens to be). The second line runs the `makegen` tool with the `<config-name>.json` settings as input. The resulting genealogy will be created in the `makegen_output/` directory. It will automatically be named to match the `name` entry in the config file..

## Server

Much of the functionality of `makegen` can be offered on a website. The code for this is in the `server` folder, and the server can bs started with `start_server.py`.
