# Genealogy 3

This is the third version of my simple genealogy modeller. This program creates randomized genealogies with a process influenced by several customizable parameters.

## The `makegen` tool

This tool allows easy customized running of genealogy examinations. The kinds of runs implemented so far are:

- Single Genealogy
- Single-Trait

### Dependencies

Make sure your have the following installed:

- [python3](https://www.python.org/download/releases/3.0/)
- [Graphviz](https://www.graphviz.org/) (free download)
- the numpy python library (install via `pip3 install numpy` on command line)

### Downloading

Before running anything, you will need to download this repository. I suggest doing something like the following in terminal (command line):
    
    $ cd ~/Documents/
    $ git clone https://github.com/Riib11/GenealogyModel3.git

This will create a directory named `GenealogyModel3/` in your main documents directory (`~/Document`). To use this method, you will need to have [`git`](https://git-scm.com/download/mac) installed

### Running `makegen`

1. Think of a name for your run. I'll refer to it as `<name>`
2. Create a new file `<name>.json` in the `makegen_configs/` directory.
3. Customize the settings in the json file, following the template of `template.json`.
4. Open terminal (command line) and execute the following:
    
```
    $ cd /path/to/GenealogyModel3/
    $ python3 makegen.py makegen_config/<name>.json
```

The first line navigates to the GenealogyModel3 directory (wherever it happens to be). The second line runs the `makegen` tool with the `<name>.json` settings as input. The resulting genealogy will be created in the `makegen_output/` directory. It will automatically be named to match `<name>`.