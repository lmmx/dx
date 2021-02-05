# dex ⠶ dx

`dx` is a mathematical indexer for the American Mathematical Society Graduate Studies in Mathematics
catalogue dataset (a subproject of [`dex`](https://github.com/lmmx/dex))

## Usage

To get started, follow the instructions for downloading the dataset yourself (or wait for me to
package it for distribution), then use the pre-prepared dataset loader module:

```py
from dx.dataset import series_df, abstracts, readerships, reviews, titles
```

`series_df` is a pandas DataFrame containing the metadata for multiple book series from AMS (at time of writing
775 books), while the other variables imported on the line above are Python lists extracted from
this DataFrame [provided for convenience when using this as a dataset].

```
>>> titles[0]
'The General Topology of Dynamical Systems'
>>> abstracts[0]
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

## Topic modelling

So far I've taken a few different approaches to topic modelling (all using Latent Dirichlet
Allocation), and the two sources of text are:

- abstracts (AKA 'blurb')
- table of contents (chapter and subchapter headings)

TODO: combine both of these for each book into a single corpus and model that.

Each of the following has involved doing a grid search over the value to use for `max_df`
(i.e. what top percentage of most common words to exclude in preprocessing), after which the
results can be explored by reviewing the output images.

- Model all text in the abstract for each book from `dx.dataset.abstracts`
  - This is more effective at removing all 'stopwords'
- Model all text in the abstract for each book, one subject area at a time, from `dx.dataset.abstracts_by_subject`
  - This is more insightful as to the variation within a particular sub-field (and avoids the topic
    model simply recovering an approximation to these 10 subject areas).
- Model all text in the table of contents for each book from `dx.dataset.toc`
- Model all text in the table of contents for each book, one subject area at a time, from `dx.dataset.toc_by_subject`

## Limitations

The topic modelling was initially limited by the dataset size: I've seen references to 600 being the
estimated minimum viable size of a newsgroup dataset for LDA, while shorter documents (e.g. tweets) would be on the
order of 5,000 to 10,000.

This limitation motivated the expansion of this project to the entire AMS catalogue beyond just the GSM series,
so far reaching around 2,000 titles (see detailed inventory below).

## Book series included

This was initially intended to cover the GSM (Graduate Studies in Mathematics) book series, one of
my favourite mathematical book series. The catalogue scraped here has expanded to cover other series from the AMS:

- `gsm`: [Graduate Studies in Mathematics](https://bookstore.ams.org/gsm) (212 titles)
  > "The volumes in this series are specifically designed as graduate studies texts, but are also
  > suitable for recommended and/or supplemental course reading. With appeal to both students and
  > professors, these texts make ideal independent study resources. The breadth and depth of the
  > series coverage make it an ideal acquisition for all academic libraries that support mathematics
  > programs."

- `chel`: [AMS Chelsea Publishing](https://bookstore.ams.org/chel) (220 titles)
  > "some of the most important classics
  > that were once out of print available to new generations of mathematicians and graduate students"

- `conm`: [Contemporary Mathematics](https://bookstore.ams.org/conm) (770 titles)
  > "high-quality, refereed proceedings
  > written by recognized experts in their fields maintains high scientific standards. Volumes draw
  > from worldwide conferences and symposia sponsored by the American Mathematical Society and other
  > organizations"

- `stml`: [Student Mathematical Library](https://bookstore.ams.org/stml) (91 titles)
  > "The AMS undergraduate series, the Student Mathematical Library, is for books that will spark
  > students' interests in modern mathematics and increase their appreciation for research. Books
  > published in the series emphasize original topics and approaches. The step from mathematical
  > coursework to mathematical research is one of the most important developments in a
  > mathematician's career. To make the transition successfully, the student must be motivated and
  > interested in doing mathematics rather than merely learning it."

- `surv`: [Mathematical Surveys and Monographs](https://bookstore.ams.org/surv) (264 titles)
  > "detailed expositions in current research fields... survey of the subject along with a brief"
  > "introduction to recent developments and unsolved problems"

- `amstext`: [AMS Pure and Applied Undergraduate Texts](https://bookstore.ams.org/amstext) (49 titles)
  > "intended for undergraduate post-calculus courses and, in some cases, will provide applications
  > in engineering and applied mathematics. The books are characterized by excellent exposition and
  > maintain the highest standards of scholarship. This series was founded by the highly respected
  > mathematician and educator, Paul J. Sally, Jr"

- `amsip`: [AMS/IP Studies in Advanced Mathematics](https://bookstore.ams.org/amsip) (59 titles)
  > "jointly published by the AMS and International Press, includes monographs, lecture notes,
  > collections, and conference proceedings on current topics of importance in advanced mathematics.
  > Harvard University Professor of Mathematics Shing-Tung Yau is Editor-in-Chief for the series"

- `cworks`: [Collected Works](https://bookstore.ams.org/cworks) (50 titles)
  > "presents the substantial body of work of many outstanding mathematicians. Some collections
  > include the complete works of an individual, while others feature selected papers. Readers can
  > follow the major ideas and themes that developed over the course of a given mathematicians
  > career."

- `crmp`: [CRM Proceedings & Lecture Notes](https://bookstore.ams.org/crmp) (56 titles)
  > "encompasses conference proceedings and lecture notes from important research conferences held
  > at the Centre de Recherches Mathématiques at the Université de Montréal. This series is
  > co-published by the AMS and the Centre de Recherches Mathématiques"

- `dimacs`: [DIMACS: Series in Discrete Mathematics and Theoretical Computer Science](https://bookstore.ams.org/dimacs) (76 titles)
  > "includes conference and workshop proceedings and volumes on education in discrete mathematics
  > and theoretical computer science. Volumes are derived from programs at Rutgers Universitys
  > Center for Discrete Mathematics and Theoretical Computer Science and also sponsored by Princeton
  > University, AT&T Labs Research, Bell Labs (Lucent Technologies), Cancer Institute of New Jersey
  > (CINJ), NEC Research Institute, and Telcordia Technologies."

- `hmath`: [History of Mathematics](https://bookstore.ams.org/hmath) (45 titles)
  > "compelling historical perspectives on the individuals and communities that have profoundly
  > influenced mathematics development. Each book constitutes a valuable addition to an historical
  > or mathematical book collection. Volumes 4 through 39 were co-published with the London
  > Mathematical Society. From volume 40 on, these volumes are published by the AMS."

- `text`: [AMS/MAA Textbooks](https://bookstore.ams.org/text) (56 titles)
  > "cover all levels of the undergraduate curriculum with a focus on textbooks for upper-division
  > students. They are written by college and university faculty and are carefully reviewed by an
  > editorial board of teaching faculty"


With only a few omitted due to technicalities, the total dataset size is currently 1935 of 1963 titles
(so approaches the 2000 title mark, a reasonable size, and about an order of magnitude larger than
the initial dataset!)

## Extension to MSC

The AMS website includes topics from the Mathematical Subject Classification (MSC) which would be
interesting to either validate or to explore through the topic models (i.e. cross-reference the
latent topics defined by LDA with the MSC labels).

## Extension to subject indexes

Additionally, I'd really like to see the indexes added as the 'documents' for topic modelling
(simply removing the page numbers and collapsing the list into a single string would suffice).

This would probably require further preprocessing (but in many cases it's available from images
and this can be OCR'd reasonably well with `tesseract`). That might come more under "labour of
love" than I'm currently willing to do!

## Reparsing

If you make a change to the parser, run `dx.dataset.reparse_all_series()` to check it's working as expected,
and `dx.dataset.reparse_all_series(overwrite_pickles=True)` to overwrite them. Alternatively, just overwrite
after backing up your pickles (a simple shell script `back_up_pickles.sh` is included to do so).
