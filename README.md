# uh_transcript_parser
A simple parsing tool to convert a University of Helsinki transcript of studies into CSV. 
This tool is meant to speed up the process of reviewing stipend applications.


## Requirements
- Python 3.x (tested with 3.11)
  - No additional libraries needed
- poppler-utils (to convert PDF to text)

## Usage

### Converting PDF File to Text (Debian/Ubuntu)

Installing poppler-utils:
```bash
sudo apt install poppler-utils
```

Converting pdf to text:
```bash
pdftotext -layout file.pdf
```

Bulk conversion from pdf to text. Suppose you have all PDF files in a directory named `pdf_files` and 
the text files will be put into directory `text_files`:
```bash
for file in pdf_files/*.pdf; do pdftotext -layout "$file" "text_files/$(basename "$file" .pdf).txt"; done
```

### Running the parser

Convert a single file (bash or powershell):
```bash
python main.py file.txt output_directory/
```

Bulk Conversion (bash). Suppose you have all text files in a directory named `text_files` and
the CSV files will be put into directory `csv_files`:
```bash
for file in text_files/*.txt; do python main.py "$file" csv_files/; done
```

### Reading the CSV
You can open the CSV files with any spreadsheet software (e.g. LibreOffice Calc, Excel). 
Comma `,` is used as the delimiter and the encoding is UTF-8.

If the run is successful, the number of calculated credits (Parserin laskemat opintopisteet) 
and the number of credits in the transcript (Opintopisteitä yhteensä) should match. 
The total points for the review is displayed after column `Arvostelupisteet`. 