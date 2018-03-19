# extract-pages

### Create conda env:
```
conda create -yn extract-pages python=3.6
conda activate extract-pages
pip install -r requirements.txt
```

### Usage:
```
$ python extract_pages.py -h
usage: extract_pages.py [-h] [-i INPUT_FILES [INPUT_FILES ...]]
                        [-p PAGES [PAGES ...]] [-o OUTPUT_FILE]

Extract and combine pages from multiple pdf files

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILES [INPUT_FILES ...], --input-files INPUT_FILES [INPUT_FILES ...]
                        blank-separated input pdf-file list
  -p PAGES [PAGES ...], --pages PAGES [PAGES ...]
                        blank-separated list of pages list
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        output file name
```

### Example:
```
$ python extract_pages.py -i input.pdf -p 1,3-6 -o output.pdf
```
