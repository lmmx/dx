# dex ⠶ dx

`dx` is a mathematical indexer for the American Mathematical Society Graduate Studies in Mathematics
catalogue dataset (a subproject of [`dex`](https://github.com/lmmx/dex))

## Usage

To get started, follow the instructions for downloading the dataset yourself (or wait for me to
package it for distribution), then use the pre-prepared dataset loader module:

```py
from dx.lda.dataset import gsm_df, abstracts, readerships, reviews, titles
```

`gsm_df` is a pandas DataFrame containing the entire published catalogue's metadata (at time of writing),
while the other variables imported on the line above are pandas Series extracted from this DataFrame,
provided for convenience.

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
