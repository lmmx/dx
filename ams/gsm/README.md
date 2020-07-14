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

## TBD: to be developed

- Run `crawl.py` without `dry_run=True` after setting up some sort of `pickle` or HTML file writing
  - Preferable to store [even temporarily] as the full crawl takes half an hour with the required delay
- After downloading the pages, categorise each volume the page describes, using the `topics` dict
  imported from `parse_topics.py`
