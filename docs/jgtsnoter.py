import csv
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import hashlib

# Create directory if not exists
if not os.path.exists('./_snote_content_cache'):
    os.makedirs('./_snote_content_cache')

with open('jgtsnoter.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    links = []

    for row in csv_reader:
        url = row[0]
        links.append(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create a hash of the URL to use as the filename
        url_hash = hashlib.md5(url.encode()).hexdigest()

        # Save the HTML content into a file
        with open(f'./_snote_content_cache/{url_hash}.html', 'w') as html_file:
            html_file.write(soup.prettify())

        # Download images
        for img in soup.find_all('img'):
            img_url = urllib.parse.urljoin(url, img['src'])
            img_filename = hashlib.md5(img_url.encode()).hexdigest()
            img_response = requests.get(img_url)

            with open(f'./_snote_content_cache/{img_filename}', 'wb') as img_file:
                img_file.write(img_response.content)

    # Create index-snote.md
    with open('index-snote.md', 'w') as md_file:
        for link in links:
            url_hash = hashlib.md5(link.encode()).hexdigest()
            md_file.write(f'- [{link}](./_snote_content_cache/{url_hash}.html)\n')