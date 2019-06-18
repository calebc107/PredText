# predText
A predictive-text algorithm using machine learning via Markov Chains.
Input data is taken from Reddit.com's newest comments (old.reddit.com/r/all/comments/), then each sentence is analyzed and each word is put in a dictionary. This dictionary keeps track of which words are most likely to come after two root words, allowing for vaguely coherent sentence structures.
## Installation
These sctipts can be used in place as-is, but your python environment should be 3.6 with blist and ujson installed. You can install them with `pip3 install blist ujson`
## Usage
Simply run `./init.py` so that the input data can be downloaded. Once that is complete then `./start.py` can be run to generate sentences.
