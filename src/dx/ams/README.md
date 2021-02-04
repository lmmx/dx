An overview of the different book code formats (parsed in `scraper/crawler.py` for each series):

- GSM: int, "R" suffixes (default)
- CHEL: float, "H" suffixes
- CONM: float, "R" suffixes (default)
- STML: float, "R" suffixes (default)
- SURV: float, "S" suffixes

- AMSTEXT: int, "R" suffixes (default)
- AMSIP: float, "R" suffixes (default)
- CWORKS: float, "R" suffixes (default)
- CRMP: int, "R" suffixes (default)
- DIMACS: int, "R" suffixes (default)
- HMATH: int, "R" suffixes (default)
- TEXT: int, "R" suffixes (default)

## Summary of how to add new modules

- `cp -r gsm/ newmodule` (copy a template over e.g. the `gsm` module)
- `cd newmodule` (or whatever you've called the new module)
- `rm store/*.{html,p}` (delete pickles and HTML files, etc.)
- `> data/book-series-number-listing.csv` blank the book listing
- `cat scraper/product_code_check.js | xclip -sel clip`
  - Modify this script if product codes end in a letter other than "R".
- Open the browser at the URL of the book series (https://bookstore.ams.org/SERIES)
- Open the element inspector then switch to the console, paste in the contents of
  `product_code_check.js` copied above
- Return to the terminal and run `xclip -o >> data/book-series-number-listing.csv`
- Repeat the last two steps repeatedly until after pasting in the data from the final
  page of the book series
- Change the `series_suffix` (`scraper.crawler` line 69) to the new module, and the
  `reprint_suffix` if the book product codes end in letters other than "R".
- Run the following (changing 'newmodule' to the actual name you're using):

```py
pages, parsed_pages = dx.ams.newmodule.scraper.crawl()
vol_str = "-".join([parsed_pages[i].metadata.metadoc.volume for i in (0,-1)])
pickle_name = f"newmodule-{vol_str}_responses_and_parsings.p"
dx.ams.newmodule.scraper.store_as_pickle((pages, parsed_pages), pickle_name)
```

- Either print out the value of `pickle_name` or look in the module's `store/` directory,
  and make this the default value passed to `responses_and_reparsed` in `scraper.reparser`
- Update the README of the new module and remove all references to the template module
  (search for "gsm" and modify), and also record the pickle location in there
- In `dx.lda.dataset`:
  - Import the new module's `reparser`⠶`responses_and_reparsed` function as `newmodule_results`
  - Add an entry for `newmodule_df` into `__all__`
  - Add an entry into the `series_pages` dict and another into `series_df_dict`

The new module's scraped data will now be included in the dataset!
