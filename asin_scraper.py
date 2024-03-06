# Author: Andrew Sisson
# Date: 03-23-2023
# Description: This script scrapes the Amazon product pages for a list of URLs and returns the ASINs (Amazon Standard Identification Numbers) for each URL. It also returns the number of unique ASINs for each URL.
# Usage: GPT-3 Web Scraping, Python
# Credits: Github Co-Pilot, OpenAI, Stack Overflow, Google, and the Python community

import datetime
import re
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd
import multiprocessing as mp
import io

# URL of the CSV file containing the list of articles to scrape
ARTICLES_LIST_URL = "https://docs.google.com/spreadsheets/d/1LlDjuC01tUojnVR3xgnW-3tPgePqlFhlvULrQ5fa_iI/export?format=csv"

# Number of processes to use for multiprocessing
NUM_PROCESSES = mp.cpu_count()

# Get the list of articles to scrape from the specified CSV file
def get_articles():
    response = requests.get(ARTICLES_LIST_URL)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text))
    return df

# Scrape the Amazon product page for the given URL and return the ASIN (Amazon Standard Identification Number) if found
def get_asin(article_url):
    try:
        response = requests.get(article_url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        asin_tags = soup.find_all("a", href=lambda href: href and "amazon.com" in href)
        asins = []
        for asin_tag in asin_tags:
            url = asin_tag.get("href")
            asin = re.findall(r"(?:/dp/|/product/)([A-Za-z0-9]{10})", url)
            if asin:
                print(f"Found ASIN {asin[0]} for URL {article_url}")
                asins.append(asin[0])
        if not asins:
            print(f"No ASIN found for URL {article_url}")
        return asins
    except (RequestException, ValueError):
        print(f"Error scraping URL {article_url}")
        return None

# Scrape the Amazon product pages for the given list of article URLs and return a list of ASINs
# Uses multiprocessing to speed up the scraping process
def scrape_articles(article_urls):
    manager = mp.Manager()
    progress_queue = manager.Queue()
    pool = mp.Pool(NUM_PROCESSES)
    results = []
    for article_url in article_urls:
        results.append(pool.apply_async(get_asin, args=(article_url,)))

    pool.close()
    pool.join()

    asins = []
    for result in results:
        asin_list = result.get()
        if asin_list is not None:
            asins.append(asin_list)
        else:
            asins.append([])

    num_asins = sum(len(a) for a in asins)
    num_urls = len(article_urls)
    print(f"Found {num_asins} ASINs out of {num_urls} URLs")
    return asins

# Get the positions of the ASINs for each article URL and save them to a CSV file
def get_asin_positions():
    articles_df = get_articles()
    article_urls = articles_df["Live URL"].tolist()
    asins = scrape_articles(article_urls)
    positions = articles_df["Live URL"].apply(lambda x: article_urls.index(x) if x in article_urls else None)
    data = []
    for i, asin_list in enumerate(asins):
        url = article_urls[i]
        for asin in asin_list:
            data.append([url, asin])
    df = pd.DataFrame(data, columns=["URL", "ASIN"])
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"asin_positions_{timestamp}.csv"
    df.to_csv(output_file, index=False)

# Get the number of unique ASINs for each article URL and save them to a CSV file
def get_unique_asins():
    df = pd.read_csv("asin_positions.csv")
    counts = df.groupby("URL")["ASIN"].nunique()
    df = pd.DataFrame({"URL": counts.index, "Count": counts.values})
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"unique_asins_{timestamp}.csv"
    df.to_csv(output_file, index=False)

# Main function
if __name__ == "__main__":
    try:
        get_asin_positions()
        get_unique_asins()
    except Exception as e:
        print("An error occurred:", str(e))
