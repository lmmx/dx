# dex ⠶ dx

`dx` is a mathematical indexer for the American Mathematical Society Graduate Studies in Mathematics
catalogue dataset (a subproject of [`dex`](https://github.com/lmmx/dex))

## Usage

To get started, follow the instructions for downloading the dataset yourself (or wait for me to
package it for distribution), then use the pre-prepared dataset loader module:

```py
from dx.lda.dataset import gsm_df, abstracts, readerships, reviews, titles
```

`gsm_df` is a pandas DataFrame containing the metadata for the AMS GSM series (at time of writing
207 books), while the other variables imported on the line above are pandas Series extracted from
this DataFrame, provided for convenience.

```
>>> titles.tolist()[0]
'The General Topology of Dynamical Systems'
>>> abstracts.tolist()[0]
"Topology, the foundation of modern analysis, arose historically as a way to organize ideas like
compactness and connectedness which had emerged from analysis. Similarly, recent work in dynamical
systems theory has both highlighted certain topics in the pre-existing subject of topological
dynamics (such as the construction of Lyapunov functions and various notions of stability) and also
generated new concepts and results (such as attractors, chain recurrence, and basic sets). This book
collects these results, both old and new, and organizes them into a natural foundation for all
aspects of dynamical systems theory. No existing book is comparable in content or scope. Requiring
background in point-set topology and some degree of “mathematical sophistication”, Akin's book
serves as an excellent textbook for a graduate course in dynamical systems theory. In addition,
Akin's reorganization of previously scattered results makes this book of interest to mathematicians
and other researchers who use dynamical systems in their work."
```

To model the titles with LDA:

```py
from dx.lda.plot_lda_topics_example import plot_lda
plot_lda()
```

## Limitations

The topic modelling is undoubtedly limited by the dataset size: I've seen references to 600 being the
rough size of a newsgroup dataset for LDA, while shorter documents (e.g. tweets) would be on the
order of 5,000 to 10,000.

Regardless of what the precise figure is, this limitation motivates the expansion of this project to
the entire AMS catalogue (beyond just the GSM series).

## Other book series to include

In addition to the GSM, the AMS have several other book series given below by their series code
(alongside the number of titles in the series, top 3 in bold):

- **chel: 200**
- amstext: 49
- amsip: 59
- cworks: 50
- **conm: 770**
- crmp: 56
- dimacs: 76
- hmath: 45
- **surv: 264**
- stml: 91
- text: 56

These series total a further 1736 titles, and are broadly not too different from the approach of
the GMS series, so would make a suitable extension to the dataset.

The top 3 (`chel`, `conm`, `surv`) make up the majority: 1254 of 1736 (or 72%), and so would be
the best candidates for a first attempt to enlarge the dataset. These are:

- [AMS Chelsea Publishing](https://bookstore.ams.org/chel):
  > "some of the most important classics
  > that were once out of print available to new generations of mathematicians and graduate students"

- [Contemporary Mathematics](https://bookstore.ams.org/conm): 
  > "high-quality, refereed proceedings
  > written by recognized experts in their fields maintains high scientific standards. Volumes draw
  > from worldwide conferences and symposia sponsored by the American Mathematical Society and other
  > organizations"

- [Mathematical Surveys and Monographs](https://bookstore.ams.org/surv):
  > "detailed expositions in current research fields... survey of the subject along with a brief"
  > "introduction to recent developments and unsolved problems"
