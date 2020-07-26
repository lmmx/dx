# dx » ams » gsm

- AMS: "American Mathematical Society"
  - GSM: "Graduate Studies in Mathematics"
    - URL: [https://bookstore.ams.org/gsm](https://bookstore.ams.org/gsm)

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
  - There are a few undesired and awkward values (left in this CSV), the final total is 207 books.

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
decided I don't care about] is stored in a `AMSGSMInfoPage` object (see `soup_structure.py`).

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

## TBD: to be developed

- Run `crawl.py` without `dry_run=True` after setting up some sort of `pickle` or HTML file writing
  - Preferable to store [even temporarily] as the full crawl takes half an hour with the required delay
- After downloading the pages, categorise each volume the page describes, using the `topics` dict
  imported from `parse_topics.py`
