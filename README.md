# ASIN Scraper
  
  This is a Python script for scraping ASINs (Amazon Standard Identification Numbers) from a list of article URLs.

# Requirements
  
  This script requires the following Python packages:

   requests
   beautifulsoup4
   pandas
   multiprocessing
 
These packages can be installed using pip:

   pip install requests beautifulsoup4 pandas

# Usage
 
  First, you need to create a Google Sheets document containing a list of article URLs. The URLs should be in a column labeled "Live URL". You can also include other columns in the sheet with additional information about the articles.

  Export the sheet as a CSV file and make a note of the URL.

  Modify the ARTICLES_LIST_URL variable in the script to point to the URL of the CSV file.

  Run the script:
   
    python asin_scraper.py

  The script will scrape ASINs from the URLs in the CSV file and save them to a new CSV file named asin_positions_<timestamp>.csv, where <timestamp> is the current date and time.

  The script will read the asin_positions_<timestamp>.csv file and count the number of unique ASINs for each article, saving the results to a new CSV file named unique_asins_<timestamp>.csv.

# Author: Andrew Sisson
# Description: This script scrapes the Amazon product pages for a list of URLs and returns the ASINs (Amazon Standard Identification Numbers) for each URL. It also returns the number of unique ASINs for each URL.
# Usage: GPT-3 Web Scraping, Python
# Credits: Github Co-Pilot, OpenAI, Stack Overflow, Google, and the Python community
