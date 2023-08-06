Transition-based UCCA Parser
============================
TUPA is a transition-based parser for [Universal Conceptual Cognitive Annotation (UCCA)][1].

### Requirements
* Python 3.6

### Install

Create a Python virtual environment. For example, on Linux:
    
    virtualenv --python=/usr/bin/python3 venv
    . venv/bin/activate              # on bash
    source venv/bin/activate.csh     # on csh

Install the latest release:

    pip install tupa

Alternatively, install the latest code from GitHub (may be unstable):

    git clone https://github.com/danielhers/tupa
    cd tupa
    pip install .

Train the parser
----------------

Having a directory with UCCA passage files
(for example, [the English Wiki corpus](https://github.com/UniversalConceptualCognitiveAnnotation/UCCA_English-Wiki)),
run:

    python -m tupa -t <train_dir> -d <dev_dir> -c <model_type> -m <model_filename>

The possible model types are `sparse`, `mlp`, and `bilstm`.

### Parse a text file

Run the parser on a text file (here named `example.txt`) using a trained model:

    python -m tupa example.txt -m <model_filename>

An `xml` file will be created per passage (separate by blank lines in the text file).

### Pre-trained models

To download and extract [a model pre-trained on the Wiki corpus](https://github.com/huji-nlp/tupa/releases/download/v1.3.10/ucca-bilstm-1.3.10.tar.gz), run:

    curl -LO https://github.com/huji-nlp/tupa/releases/download/v1.3.10/ucca-bilstm-1.3.10.tar.gz
    tar xvzf ucca-bilstm-1.3.10.tar.gz

Run the parser using the model:

    python -m tupa example.txt -m models/ucca-bilstm
    
### Other languages

To get [a model](https://github.com/huji-nlp/tupa/releases/download/v1.3.10/ucca-bilstm-1.3.10-fr.tar.gz) pre-trained on the [French *20K Leagues* corpus](https://github.com/UniversalConceptualCognitiveAnnotation/UCCA_French-20K)
or [a model](https://github.com/huji-nlp/tupa/releases/download/v1.3.10/ucca-bilstm-1.3.10-de.tar.gz) pre-trained on the [German *20K Leagues* corpus](https://github.com/UniversalConceptualCognitiveAnnotation/UCCA_German-20K), run:

    curl -LO https://github.com/huji-nlp/tupa/releases/download/v1.3.10/ucca-bilstm-1.3.10-fr.tar.gz
    tar xvzf ucca-bilstm-1.3.10-fr.tar.gz
    curl -LO https://github.com/huji-nlp/tupa/releases/download/v1.3.10/ucca-bilstm-1.3.10-de.tar.gz
    tar xvzf ucca-bilstm-1.3.10-de.tar.gz

Run the parser on a French/German text file (separate passages by blank lines):

    python -m tupa exemple.txt -m models/ucca-bilstm-fr --lang fr
    python -m tupa beispiel.txt -m models/ucca-bilstm-de --lang de

Using BERT
----------
BERT can be used instead of standard word embeddings.
First, install the required dependencies:

    pip install -r requirements.bert.txt
    
Then pass the `--use-bert` argument to the training command.

See the possible configuration options in `config.py` (relevant options have the prefix `bert`).

### BERT Multilingual Training
A multilingual model can be trained, to leverage
cross-lingual transfer and improve results on low-resource languages:

1. Make sure the input passage files have the `lang` attribute. See the script [`set_lang`](https://github.com/huji-nlp/semstr/blob/master/semstr/scripts/set_lang.py) in the package `semstr`.
2. Enable BERT by passing the `--use-bert` argument.
3. Use the multilingual model by passing `--bert-model=bert-base-multilingual-cased`.
4. Pass the `--bert-multilingual=0` argument to enable multilingual training.

### BERT Performance
Here are the average results over 3 BERT multilingual models trained on the [German _20K Leagues_ corpus](https://github.com/UniversalConceptualCognitiveAnnotation/UCCA_German-20K),
[English Wiki corpus](https://github.com/UniversalConceptualCognitiveAnnotation/UCCA_English-Wiki) 
and only on 15 sentences from the [French _20K Leagues_ corpus](https://github.com/UniversalConceptualCognitiveAnnotation/UCCA_French-20K), 
with the following settings:
```
bert-model=bert-base-multilingual-cased
bert-layers=-1 -2 -3 -4
bert-layers-pooling=weighted
bert-token-align-by=sum
```
The results:

| description          | test primary F1 | test remote F1 | test average |
| --------------------  | ------------------- | --------------- | ---------------- |
| German 20K Leagues |      0.828           |     0.6723        |    0.824          |
| English 20K Leagues |      0.763           |     0.359        |    0.755          |
| French 20K Leagues |      0.739           |     0.46        |    0.732          |
| English Wiki |      0.789           |     0.581        |    0.784          |

*[English _20K Leagues_ corpus](https://github.com/UniversalConceptualCognitiveAnnotation/UCCA_English-20K) is used as out of domain test.

### Pre-trained Models with BERT

To download and extract [a multilingual model](https://github.com/huji-nlp/tupa/releases/download/v1.4.0/bert_multilingual_layers_4_layers_pooling_weighted_align_sum.tar.gz) trained with the settings above, run:

    curl -LO https://github.com/huji-nlp/tupa/releases/download/v1.4.0/bert_multilingual_layers_4_layers_pooling_weighted_align_sum.tar.gz
    tar xvzf bert_multilingual_layers_4_layers_pooling_weighted_align_sum.tar.gz

To run the parser using the model, use the following command. Pay attention that you need to replace `[lang]` with
 the right language symbol (`fr`, `en`, or `de`):

    python -m tupa example.txt --lang [lang] -m bert_multilingual_layers_4_layers_pooling_weighted_align_sum

Author
------
* Daniel Hershcovich: daniel.hershcovich@gmail.com

Contributors
------------
* Ofir Arviv: ofir.arviv@mail.huji.ac.il


Citation
--------
If you make use of this software, please cite [the following paper](http://aclweb.org/anthology/P17-1104):

    @InProceedings{hershcovich2017a,
      author    = {Hershcovich, Daniel  and  Abend, Omri  and  Rappoport, Ari},
      title     = {A Transition-Based Directed Acyclic Graph Parser for {UCCA}},
      booktitle = {Proc. of ACL},
      year      = {2017},
      pages     = {1127--1138},
      url       = {http://aclweb.org/anthology/P17-1104}
    }

The version of the parser used in the paper is [v1.0](https://github.com/huji-nlp/tupa/releases/tag/v1.0).
To reproduce the experiments, run:

    curl -L https://raw.githubusercontent.com/huji-nlp/tupa/master/experiments/acl2017.sh | bash
    

If you use the French, German or multitask models, please cite
[the following paper](http://aclweb.org/anthology/P18-1035):

    @InProceedings{hershcovich2018multitask,
      author    = {Hershcovich, Daniel  and  Abend, Omri  and  Rappoport, Ari},
      title     = {Multitask Parsing Across Semantic Representations},
      booktitle = {Proc. of ACL},
      year      = {2018},
      pages     = {373--385},
      url       = {http://aclweb.org/anthology/P18-1035}
    }

The version of the parser used in the paper is [v1.3.3](https://github.com/huji-nlp/tupa/releases/tag/v1.3.3).
To reproduce the experiments, run:

    curl -L https://raw.githubusercontent.com/huji-nlp/tupa/master/experiments/acl2018.sh | bash


License
-------
This package is licensed under the GPLv3 or later license (see [`LICENSE.txt`](LICENSE.txt)).

[1]: http://github.com/huji-nlp/ucca


[![Build Status (Travis CI)](https://travis-ci.org/danielhers/tupa.svg?branch=master)](https://travis-ci.org/danielhers/tupa)
[![Build Status (AppVeyor)](https://ci.appveyor.com/api/projects/status/github/danielhers/tupa?svg=true)](https://ci.appveyor.com/project/danielh/tupa)
[![Build Status (Docs)](https://readthedocs.org/projects/tupa/badge/?version=latest)](http://tupa.readthedocs.io/en/latest/)
[![PyPI version](https://badge.fury.io/py/TUPA.svg)](https://badge.fury.io/py/TUPA)
