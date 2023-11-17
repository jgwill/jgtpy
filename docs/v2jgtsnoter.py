# IMPORTANT NOTE: This is a simplified example and might not work correctly 
# without further adjustments. It also does not include error handling and 
# might exceed the rate limits or the maximum input size of the OpenAI API.

import csv
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import hashlib
import json
from openai import OpenAI


# Set the OpenAI API key
import os
from dotenv import load_dotenv

# Load .env file from the current directory
load_dotenv()

# If the OPENAI_API_KEY is not found, try to load it from the .env file in the HOME directory
if 'OPENAI_API_KEY' not in os.environ:
    home_dir = os.path.expanduser("~")
    load_dotenv(os.path.join(home_dir, '.env'))
api_key=os.getenv('OPENAI_API_KEY')


client = OpenAI(api_key=api_key)


# The rest of your code...

# Create directory if not exists
if not os.path.exists('./_snote_content_cache'):
    os.makedirs('./_snote_content_cache')

# Load summaries and hashes of previously processed URLs, if the file exists
try:
    with open('./_snote_content_cache/data.json', 'r') as data_file:
        data = json.load(data_file)
except FileNotFoundError:
    data = {}

with open('jgtsnoter.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    link_titles = []

    for row in csv_reader:
        url = row[0]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title of the page
        title = soup.title.string if soup.title else url
        print("Processing: " +title + " :: " + url)
        # Store the link and its title
        link_titles.append((url, title))

        # Create a hash of the URL to use as the filename
        url_hash = hashlib.md5(url.encode()).hexdigest()

        # Hash the content of the page
        content_hash = hashlib.md5(response.text.encode()).hexdigest()

        # If the content has changed or it's a new URL, save the new content and get a new summary
        if url not in data or data[url]['hash'] != content_hash:
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

            # Get a summary of the new content
            prompt_text = response.text[:5000]
            completion = client.completions.create(
                model="text-davinci-002",
                prompt=prompt_text,
                temperature=0.3,
                max_tokens=100
            )

            new_summary = completion.choices[0].text.strip() if completion.choices else ""

            # If the URL was processed before, identify changes
            changes = ''
            if url in data:
                old_summary = data[url]['summary']
                # This is a simple way to identify changes and might not work well for complex text
                changes = ' '.join(set(new_summary.split()) - set(old_summary.split()))

            # Update the data of the URL
            data[url] = {'hash': content_hash, 'summary': new_summary, 'changes': changes}

    # Save the data of the processed URLs
    with open('./_snote_content_cache/data.json', 'w') as data_file:
        json.dump(data, data_file)

    # Create index-snote.md
    with open('index-snote.md', 'w') as md_file:
        md_file.write('| Title | Summary | Changes |\n')
        md_file.write('|-------|---------|---------|\n')
        for link, title in link_titles:
            url_hash = hashlib.md5(link.encode()).hexdigest()
            summary = data[link]['summary'] if link in data else ''
            changes = data[link]['changes'] if link in data else ''
            md_file.write(f'| [{title}](./_snote_content_cache/{url_hash}.html) | {summary} | {changes} |\n')