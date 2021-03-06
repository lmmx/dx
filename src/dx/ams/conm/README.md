# dx » ams » conm

Data submodule in the `dx` package (to be shipped with the scraped dataset in future release)

- AMS: "American Mathematical Society"
  - CONM: "Contemporary Mathematics"
    - URL: [https://bookstore.ams.org/conm](https://bookstore.ams.org/conm)

## Manifest

- `parse_subject_form.js` is a 3 line Javascript script run in the browser console at the URL above
  which copies the list of topic shortnames and full names to the clipboard

  - `topics.csv` is a double-quoted comma-separated list of the 9 topics (not including "all")

    - `parse_topics.py` opens this CSV and instantiates a `dict` of these shortnames to
      full category names

- `product_code_check.js` was run repeatedly in a browser console at the AMS GSM URL above,
  followed by `xclip -o >> book-series-number-listing.csv` each time

- `book-series-number-listing.csv` is a CSV of the 210 book [volume] numbers acquired in this way,
  along with a boolean indicating whether the book is a reprint (in which case its code will be
  suffixed with `.R` and the book's URL will be suffixed with `-r`)
  - There are a few undesired and awkward values (left in this CSV), the final total is 770 books.

- `crawler.py` downloads all of the pages for the listed books (ignoring the 2
  aforementioned exceptions)

## Crawler download handling

All downloads will be handled in a single `requests.Session` instance (in `crawler.py`)

Restarting will be permitted by proceeding through the volume listing in sorted order,
thus enabling a `initialise_at` parameter (default: `1`) to enable starting from any
given volume number

- e.g. to resume an interrupted download or to fix some particular value

Crawling a specific set of pages will be permitted by a `volumes` parameter (default:
`None`) which will, if provided, override the consecutive iterator and instead only
iterate through the [string] keys whose numeric value equals those in the `volumes`
argument

- e.g. `GET_book_metadata_pages(initialise_at=4, volumes=range(1,10,3)` will
  use the `volumes` iterator which gives values `1,4,7`, and omit the value `1`
  due to the `initialise_at` parameter.

Crawling is done manually (so as to inspect and fix errors) and then the results are pickled:

```py
import dx
pages, parsed_pages = dx.ams.conm.scraper.crawl()
vol_str = "-".join([parsed_pages[i].metadata.metadoc.volume for i in (0,-1)])
pickle_name = f"conm-{vol_str}_responses_and_parsings.p"
dx.ams.conm.scraper.store_as_pickle((pages, parsed_pages), pickle_name)
```

## Metadata

Each page contains the standard book metadata:
- author(s) [always]
  - [always] order of names
  - [sometimes] institutional affiliation
- page count [always]
- table of contents
  - page numbers for:
    - [always] chapter numbers
    - [sometimes] chapter titles
    - [sometimes] subsection numbers/titles
- year of publication [always]
- list price (print) [always]
- sale price (ebook) [always?]
- book cover photo thumbnail [always]

As well as 'secondary' metadata, relating to guidance on usage of the material:
- suggested readership (semicolon-separated list) [sometimes]
- reviews and endorsements [always?]
  - review (free text)
  - reviewer [name and/or organisation/institution]

As well as more circumstantial info (with which to make a nice library-like interface):
- which book chapters are available as free samples [sometimes]

## Metadata storage

The metadata (as well as some more details like ISBN) above [except for the ebook price which I
decided I don't care about] is stored in a `AMSBookInfoPage` object (see `soup_structure.py`).

- The `content` attribute on this object stores a `ContentSection` object, which now has only a single property:
  - `cover_image` which is a string, the URL suffix at _https://bookstore.ams.org_ of the cover image JPG file
  - There is no other content on the page needed, the rest is all stored in metadata (this feels
    sensible to me as this is the only 'presentational' piece of info)
- The `metadata` attribute on this object stores a `TextInfoSection` object with 7 attributes:
  - `title` is a string of the title text
  - `abstract` is a string of the abstract text
  - `readership` is a string of the 'readership' statement text
  - `reviews` is a `Reviews` (list) object, each item in which is a `ReviewEntry` object
  - `metadoc` is a `MetaDoc` object with 11 to 13 attributes (it depends on each book) out of:
    - `authors` is a list of strings (the author names)
    - `affiliation` is a list of affiliated institutions for each author (may not be given)
    - `volume` is a string of the volume number (e.g. '2' for GSM-2)
    - `publicationmonthyear` is the [YYYY-MM-DD formatted] date of publication
    - `copyrightyear` is the year of copyright (presumably matches `publicationmonthyear` YYYY)
    - `pagecount` is an integer number of pages the book has (presumably matches the max.
      `pageno` in the table of contents)
    - `covertype` is a string of the type of hardback (presumably all in this series will be
      'Hardcover')
    - `isbn13print` is a string of the ISBN13 code for the print book
    - `mscprimary` is a list of one or more primary Mathematics Subject Classification codes for the
      book
    - `mscsecondary` is a list of one or more secondary Mathematics Subject Classification codes for
      the book (not always given, sometimes only `mscprimary` is)
    - `appliedmath` is a boolean of whether the book is about an applied topic
    - `subject` is a list of `Topic` objects (internally called 'SXG' subject code, corresponding to
      the topic list from the `parse_topics.py` module) with a shortname (`code` string attribute) and
      a long name (`fullname` string attribute)
    - `printprice1` is a string of the price (presumably should all be around '45.00' to '50.00')
  - `toc_info` is a `TocInfo` object representing the table of contents, with a `toc_entries` attribute
    which is a `TocEntries` (list) object, each item in which is a `TocEntry` object with the attributes:
    - `is_free` is a boolean of whether the the chapter entry is free to read
    - `logical_pageno` is a string of the 'internal' book page number, e.g. the cover is 'Cover1'
      and then the following pages are Roman numerals.
    - `pageno` is a string of the 'objective' book page number, starting at 1 for the cover page
    - `title` is a `TocTitle` object which has attributes:
      - `title_text` which is the 'input string' which generated the `TocTitle` object
      - `ch_num` is either `None` if the chapter is unnumbered or a `TocChapNum` object, the chapter number
        - `substr` is a string attribute for the substring within the title for the sub/chapter number
          (e.g. "1." or "2.6.")
        - `numeric` is a tuple of one or more integers (e.g. `(1,)` or `(2,6)`)
      - `ch_title_postnum` is the title substring after the chapter number (or `None` if unnumbered)
      - `symbol_groups` is a tree parsed representation `SymbolGroup` object (with a simple dict in
        `SymbolGroup.formula.parsed.statement` and the original substring in
        `SymbolGroup.formula.string`) which can easily [later] be used to create a LaTeX symbol format.

## Parsing

- [x] Run `crawl.py` without `dry_run=True` after setting up some sort of `pickle` or HTML file writing
  - Preferable to store [even temporarily] as the full crawl takes half an hour with the required delay
- [x] After downloading the pages, categorise each volume the page describes, using the `topics` dict
  imported from `parse_topics.py`

The pages are all parsed (see the `reparse` function in `crawler`⠶`reparser.py`), and stored as a
pickle (`store`⠶`conm-1-763_responses_and_parsings.p`). The helper function `responses_and_parsed`
(also in `reparser.py`) will load the variables stored in this pickle (`responses` and `reparsed`).

```py
import dx
from dx.ams.conm.scraper.reparser import responses_and_parsed
```
⇣
```py
>>> pages, parsed_pages = responses_and_parsed()
>>> parsed_pages[0]
<dx.ams.conm.scraper.soup_structure.AMSBookInfoPage object at 0x7f6635203c10>
>>>
```

## Analysis

Now the fun part!

To retrieve the parsed pages, I run:

```py
import dx
from dx.ams.conm.scraper.reparser import reparse; pages, parsed_pages, reparsed_pages = reparse()
```

Which gives a Python session with the `reparsed_pages` available to work with.

Given such a list of parsed pages (i.e. a list of `AMSBookInfoPage` objects), calling `pandas.concat` on
the `map` of the `_df_repr` over each in the list gives a single DataFrame with `NaN` values
for the missing properties unless where this absence is explicitly specified (e.g. some books in the
series don't have a table of contents so `toc_info` is `None`).

- The `sort_index(axis=1)` rearranges alphabetically rather than those columns not present in earlier entries
  becoming added as rightmost columns
- The `reset_index()` removes the singleton DataFrame row indexes (i.e. prevents all rows being indexed as `0`)

```py
page_df_list = list(map(lambda p: p._df_repr(), reparsed_pages))
df_merged = pd.concat(page_df_list).sort_index(axis=1).reset_index(drop=True)
```

```py
>>> df_merged
                                              abstract  ... volume
0    Topology, the foundation of modern analysis, a...  ...      1
1    This book presents rigidity theory in a histor...  ...      2
2    As the primary tool for doing explicit computa...  ...      3
3    This book provides an elementary, self-contain...  ...      4
4    In this book, Miranda takes the approach that ...  ...      5
..                                                 ...  ...    ...
202  This book gives a thorough and self-contained ...  ...    204
203  This book is based on notes from a beginning g...  ...    205
204  Extrinsic geometric flows are characterized by...  ...    206
205  Applied topology is a modern subject which eme...  ...    207
206  This book represents a novel approach to diffe...  ...    208

[207 rows x 19 columns]
```

The entire DataFrame can be viewed neatly using a wrapper on `pydoc.pager` (which I keep
on hand in my `~/.pythonrc`)...

- Always use `pydoc.pager` like this, it'll gum up your STDIN if called in the wrong way

```py
from pydoc import pager

def listpager(a_list):
    pager("\n".join([i if type(i) is str else repr(i) for i in a_list]))
    return
```

...and temporarily removing the limits on pandas display width:

```py
from pandas import option_context
with option_context('display.max_rows', None, 'display.max_columns', None):
    listpager([df_merged.to_string()])
```

...as long as you've exported the environment variable `$PAGER` as follows in `.bashrc`:

```sh
export PAGER='less -S'
```

If we run the following, we can view a more readable tabulated version of just the volume number,
title, and author list:

```sh
listpager([s[5:] for s in tabulate.tabulate(df_merged.loc[:, ("volume", "title", "authors")], tablefmt='psql').split("\n")])
```

For ease of access, the parsed pages and the dataframe have been pickled:

```py
from dx.ams.conm.scraper.pickle_utils import retrieve_pickle
parsed_pages, df_merged = retrieve_pickle("conm-1-763_responses_and_parsings.p")
```

For exploratory data analysis (specifically, topic modelling) the 3 most likely to produce interesting
distinguishing features are:

- abstract
- readership
- reviews

(The title will probably be too short to make good features)

---

The process of loading this data frame has been simplified for convenience:

```py
import dx
from dx.dataset import conm_df
conm_df
```
⇣
```STDOUT
                                              abstract  ... volume
0    The study of Markov random fields has brought ...  ...      1
1                                                 None  ...      2
2    The authors' purpose in writing this paper is ...  ...      3
3                                                 None  ...      4
4    This book is directed to researchers in Lie th...  ...      5
..                                                 ...  ...    ...
765  This volume is put together by the National As...  ...    759
766  This volume contains the proceedings of a conf...  ...    760
767  The Seventh ARTA (“Advances in Representation ...  ...    761
768  This book formulates a new conjecture about qu...  ...    762
769  This volume contains the proceedings of the wo...  ...    763

[770 rows x 19 columns]
```

To review the sparsity or completeness of each of these columns:

- `len([x for x in abstracts if not x])` = 23 books with a blank (`""`) or missing (`None`) abstract
- `len([x for x in readerships if not x])` = 143 books with a blank or missing readership entry
- `len([x for x in reviews if x == []])` = 747 books without a review

Abstracts should be inspected with topic models as 198/207 = 96% of the books here have them.

Readership entries are clearly not worth inspecting further as the majority of the books lack one.
