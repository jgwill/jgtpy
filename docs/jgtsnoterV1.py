import csv
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import hashlib
import json

# Create directory if not exists
if not os.path.exists('./_snote_content_cache'):
    os.makedirs('./_snote_content_cache')

# Load hashes of previously processed URLs, if the file exists
try:
    with open('./_snote_content_cache/hashes.json', 'r') as hashes_file:
        hashes = json.load(hashes_file)
except FileNotFoundError:
    hashes = {}

with open('jgtsnoter.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    link_titles = []

    for row in csv_reader:
        url = row[0]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title of the page
        title = soup.title.string if soup.title else url

        # Store the link and its title
        link_titles.append((url, title))

        # Create a hash of the URL to use as the filename
        url_hash = hashlib.md5(url.encode()).hexdigest()

        # Hash the content of the page
        content_hash = hashlib.md5(response.text.encode()).hexdigest()

        # If the content has changed or it's a new URL, save the new content
        if url not in hashes or hashes[url] != content_hash:
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

            # Update the hash of the content
            hashes[url] = content_hash
        else: # Advise skipping files that have not changed
            print(f'Skipping {url}')

    # Save the hashes of the processed URLs
    with open('./_snote_content_cache/hashes.json', 'w') as hashes_file:
        json.dump(hashes, hashes_file)

    # Create index-snote.md
    with open('index-snote.md', 'w') as md_file:
        for link, title in link_titles:
            url_hash = hashlib.md5(link.encode()).hexdigest()
            md_file.write(f'- [{title}](./_snote_content_cache/{url_hash}.html)\n')