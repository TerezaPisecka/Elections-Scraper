# Election Results Scraper (2017)

This Python script scrapes election results for selected regions in the Czech Republic from the website [volby.cz](https://www.volby.cz).

## Features
- Scrape and extract data such as code, location, registered voters, issued envelopes, valid votes and votes for each political party.
- Save the data into a structured .csv file.

## Requirements
1. Python 3.6 or higher
2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the script from the command line with two arguments:
1. **URL**: The URL of the selected election area.
2. **Output**: The name of the output CSV file.

Example:
```bash
python <script_name>.py <area_URL> <output_filename>
 ```
## Example
Election results for region Benešov:

1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
2. argument: output_Benešov.csv

```bash
python Project_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" output_Benešov.csv
 ```
Download progress:
```
Fetching main page: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
Data successfully saved to output_Benešov.csv
```
Sample of the output: 
```
code,location,registered_voters,envelopes,valid,...
529303,Benešov,13 104,8 485,8 437,1 052,10,2,624,3,802,597,109,35,112,6,11,948,3,6,414,2 577,3,21,314,5,58,17,16,682,10
532568,Bernartice,191,148,148,4,0,0,17,0,6,7,1,4,0,0,0,7,0,0,3,39,0,0,37,0,3,0,0,20,0
```
