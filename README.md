# csppinet
csppinet: A Python package for context-specific biological network construction and analysis based on omics data

```shell
 ██████ ███████ ██████  ██████  ██ ███    ██ ███████ ████████ 
██      ██      ██   ██ ██   ██ ██ ████   ██ ██         ██    
██      ███████ ██████  ██████  ██ ██ ██  ██ █████      ██    
██           ██ ██      ██      ██ ██  ██ ██ ██         ██    
 ██████ ███████ ██      ██      ██ ██   ████ ███████    ██ 
 ```
        version 1.0


- [Installation](#installing)
- [Overview](#overview)
- [Workflow](#workflow)
- [Command-line interface](#command-line-interface)
- [Python library usage](#python-library-usage)
- [Examples](#examples)
- [Article](#article)

# Installing

To build and install from source, run

```shell
python setup.py install
```
You can also install from pip with

```shell
pip install csppinet
``` 

# Overview

csppinet construct a context-specific biological network based on omics data. From omics data, such as temporal transcriptome data, csppinet generates a context-specific network for each biological condition. It provides both an easy-to-use object-oriented Python API and a command-line interface (CLI) for context-specific network construction and post-analysis. 

# Workflow

csppinet contains a flowchart designed to provide a structured context-specific (cs) network based on omics data, as well metrics and comparative reports.

csppinet features include:

        1. The construction of a context-specific network based on omics data. We account for gene activity across biological conditions, and then take this activity for each network interaction, where it remains if both genes are active;
        2. The calculation of network metrics for the genes for each context-specific network;
        3. The calculation of network metrics for each context-specific network.

# Command-line interface

csppinet can be executed from the command line using the csppinet command. It takes the network and the gene expression file, as well the number of threads (essential for large networks). 

```
usage: csppinet [-h] --network_file network.csv --expression_file gene_expression.csv --threads THREADS

optional arguments:
  -h, --help            show this help message and exit
  --network_file        A csv file containing the network
  --expression_file     A csv file containing the expression of the genes per condition
  --threads     Number of threads for multiprocessing. Considere it for large networks

example:  python3 csppinet.py --network_file network.csv --expression_file gene_expession.csv --threads 2
```
In your current working folder, csppinet generates the following outputs:

        1. A csv file containing the context-specific network for each biological condition;
        2. A csv file containing the network metrics for the genes of each context-specific network;
        3. A txt file containing the network metrics report file for each cs network. 
 
# Python library usage

csppinet generates the files in the  current working directory. 

To use as a Python library

```python

import csppinet

# csppinet arguments. Input files should be in .csv extension 
network = '/opt/data/network.csv'
exp = '/opt/data/expression_file.csv'
threads = 10

#construction
csppinet.construction(network,exp,threads)

#network metrics
csppinet.network_metrics(exp)

```

# Examples

In these examples we will use as input the network of **Saccharomyces cerevisiae** from STRINGdb with "combined_score" > 900 together with gene expression data from the article by de Carvalho, et al. 2021 (https://doi.org/10.1093/femsyr/foab030).

```shell
csppinet --network_file STRING_yeast.csv --expression_file expression_deCarvalho2021.csv --threads 10
```

# Article

For application examples, scripts and datasets access the package article on BioRxiv.
