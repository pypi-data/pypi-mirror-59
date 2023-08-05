# IMRT-QA-Data-Miner
Scans a directory for IMRT QA results.

### Quick update
Started working on a bokeh dashboard, feel free to try it out, but it's not ready for prime time.  
To try it out, set the file path of your delta4 csv output from IQDM in line 22 of trending_delta4.py
In a terminal, type:  
`bokeh serve trending_delta4.py`  
Then navigate to the link shown.  Must have the python library, bokeh, installed.  
Like-wise for trending_arccheck.py.

<img src="https://user-images.githubusercontent.com/4778878/71692503-ae78e600-2d6f-11ea-9bd6-851d9980972e.png" width='400'>

### Install
~~~~
$ pip install IQDM
~~~~

### How to run
~~~~
$ IQDM <initial-scan-dir>
~~~~

### Command line usage
~~~~
usage: IQDM [-h] [-ie] [-od OUTPUT_DIR] [-of OUTPUT_FILE] [-ver]
            [--no-recursive-search]
            [initial_directory]

Command line interface for IQDM

positional arguments:
  initial_directory     Scan this directory and all sub-directories

optional arguments:
  -h, --help            show this help message and exit  
                        
  -ie, --ignore-extension
                        Script will check all files, not just ones with .pdf
                        extensions  
                        
  -od OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output stored in local directory by default, specify
                        otherwise here  
                        
  -of OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output will be saved as <report_type>_results_<time-
                        stamp>.csv by default. Define this tag to customize
                        file name after <report_type>_  
                        
  -ver, --version       Print the IQDM version  
  
  -nr, --no-recursive-search
                        Include this flag to skip sub-directories
~~~~

### Notes
This script was written specifically for SNC Patient and Delta4, but I'd be happy to include support for other vendors 
if someone could provide some anonymized example reports.

### Vendor Compatibility
* **[Sun Nuclear](http://sunnuclear.com)**: *SNC Patient*  
    * ArcCheck compatibility contributed by [Marc Chamberland](https://github.com/mchamberland)
* **[ScandiDos](http://scandidos.com)**: *Delta4*  
This is still in beta, but the reported csv data is largely correct (reported energy might be off). The class parses much 
more data (including individual beam results), but isn't currently in csv nor validated.


### Contributing
If you'd like to contribute code to support a new vendor, please create a new python file in the parsers directory 
containing a new class. This class should include the following to be compatible:

* **PROPERTIES**
    * **identifiers**  
    this is a list of strings that collectively and uniquely are found in a report type
    * **columns**  
    a list of strings indicating the columns of the csv to be output
    * **csv**  
    a string of values for each column, delimited with DELIMITER in utilities.py
    * **report_type**  
    a string succinctly describing the report, this will be used in the results filename created in main.py

* **METHODS**
    * **process_data(text_data)**  
    processing the data does not occur until this is called
