
import csv
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# Create directory if not exists
if not os.path.exists('./_snote_content_cache'):
    os.makedirs('./_snote_content_cache')

with open('jgtsnoter.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for row in csv_reader:
        url = row[0]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Save the HTML content into a file
        with open(f'./_snote_content_cache/{urllib.parse.quote(url)}.html', 'w') as html_file:
            html_file.write(soup.prettify())