# IMPORTANT NOTE: This is a simplified example and might not work correctly 
# without further adjustments. It also does not include error handling and 
# might exceed the rate limits or the maximum input size of the OpenAI API.

import csv
import requests
from bs4 import BeautifulSoup
import html2text
import os
import urllib.parse
import hashlib
import json
from openai import OpenAI
import snoterupdate


# Set the OpenAI API key
import os
from dotenv import load_dotenv


model_to_use="text-davinci-002"




    
def save_html_content(url_hash, soup):
    with open(f'./_snote_content_cache/{url_hash}.html', 'w') as html_file:
        html_file.write(soup.prettify())

def download_images(soup, url):
    for img in soup.find_all('img'):
        img_url = urllib.parse.urljoin(url, img['src'])
        img_filename = hashlib.md5(img_url.encode()).hexdigest()
        img_response = requests.get(img_url)

        with open(f'./_snote_content_cache/{img_filename}', 'wb') as img_file:
            img_file.write(img_response.content)
            
def clean_url_response2text(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    html_text = str(soup)
    markdown_text = html2text.html2text(html_text)
    return markdown_text[:5000]
    


def get_summary(response, temperature=0.5):
    prompt_text = clean_url_response2text(response)
    completion = client.completions.create(
        model=model_to_use,
        prompt=prompt_text,
        temperature=temperature,
    )
    return completion.choices[0].text.strip() if completion.choices else ""

def get_summary_diff(new_text, old_text, temperature=0.5):
    prompt_text = f"You tell me a summary of the changes between new and old text bellow : \n\n\nNEW TEXT: {new_text}\n\nOLD TEXT: {old_text}"
    completion = client.completions.create(
        model=model_to_use,
        prompt=prompt_text,
        temperature=temperature,
    )
    return completion.choices[0].text.strip() if completion.choices else ""







# Load .env file from the current directory
load_dotenv()

# If the OPENAI_API_KEY is not found, try to load it from the .env file in the HOME directory
if 'OPENAI_API_KEY' not in os.environ:
    home_dir = os.path.expanduser("~")
    load_dotenv(os.path.join(home_dir, '.env'))
    
api_key=os.getenv('OPENAI_API_KEY')


# Create directory if not exists
if not os.path.exists('./_snote_content_cache'):
    os.makedirs('./_snote_content_cache')


client = OpenAI(api_key=api_key)



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
        # print(response.text[:5000])
        # print("---------------------------------------------------  ")
        # print(soup.prettify()[:5000])
        # print("---------------------------------------------------  ")
        
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
            save_html_content(url_hash, soup)
            download_images(soup, url)
            
            new_summary = get_summary(response)

            # If the URL was processed before, identify changes
            changes = ''
            if url in data:
                old_summary = data[url]['summary']
                # Evolved way to identify changes using AI
                changes = get_summary_diff(old_summary, new_summary)
                

            # Update the data of the URL
            data[url] = {'hash': content_hash, 'summary': new_summary, 'changes': changes, 'title': title}

    # Save the data of the processed URLs
    with open('./_snote_content_cache/data.json', 'w') as data_file:
        json.dump(data, data_file)
    

    # Call the function from snoterupdate.py
    #snoterupdate.generate_markdown(link_titles, data)
snoterupdate.generate_markdown()
    
    
    
    