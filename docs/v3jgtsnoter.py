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


# Set the OpenAI API key
import os
from dotenv import load_dotenv

import html2text
import re
import os

model_to_use = "text-davinci-002"
snoter_datasource_csv = 'jgtsnoter.csv'
snote_cache_folder_name = '_snote_content_cache'



snote_cache_folder = os.path.join(os.getcwd(), snote_cache_folder_name)

print(snote_cache_folder)
os.makedirs(snote_cache_folder, exist_ok=True)

def get_file_full_path_basename(url_hash):
    return f'{snote_cache_folder}/{url_hash}'

        
        
    
def save_html_content(url_hash, soup,title=None):
    _file_full_path_base=get_file_full_path_basename(url_hash)
    
    html_file_fullpath = _file_full_path_base + '.html'
    print("-------save_html_content----html_file_fullpath-----")
    print(html_file_fullpath)
    
    with open(html_file_fullpath, 'w') as html_file:
        html_file.write(soup.prettify())
    #Convert using html2text each soup content
    txt = html2text.html2text(str(soup))
    with open(_file_full_path_base + '.md', 'w') as txt_file:
        txt_file.write(txt)
    if title:
        #Save file with title in a subfolder in $scache_folder/bytitle
        safe_filename = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        safe_md_fullpath = os.path.join(snote_cache_folder, 'bytitle', safe_filename + '.md')
        os.makedirs(os.path.dirname(safe_md_fullpath), exist_ok=True)
        with open(safe_md_fullpath, 'w') as txt_file:
            txt_file.write(txt)
        
    

def download_images(soup, url):
    for img in soup.find_all('img'):
        img_url = urllib.parse.urljoin(url, img['src'])
        img_filename = hashlib.md5(img_url.encode()).hexdigest()
        img_response = requests.get(img_url)

        with open(f'{snote_cache_folder}/{img_filename}', 'wb') as img_file:
            img_file.write(img_response.content)

def write_to_debug_file_text(text):
    with open('debug-summary-completion.choices.txt', 'a') as f:         
         f.write("DEBUG TEXT:: " + text  + os.linesep)   

import re

def is_markdown(text):
    # Check for headers, links, lists, bold/italic text
    patterns = [
        r"^# .+",  # headers
        r"\[.+\]\(.+\)",  # links
        r"^- .+",  # lists
        r"\*.+\*",  # bold/italic text
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.MULTILINE):
            return True
    return False
def clean_url_response2text(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        html_text = str(soup)
        markdown_text = html2text.html2text(html_text)
        _res =  markdown_text[:10000]
        write_to_debug_file_text(_res)
        return _res
    except:
        try: 
            my_text = response
            
            markdown_text = my_text if is_markdown(my_text) else html2text.html2text(my_text)
            _res = markdown_text[:5000]
            write_to_debug_file_text( "DEBUG EXECEP1:" + _res)
            return _res
        except:
            write_to_debug_file_text(response)
            return response
    



def write_to_debug_file(choices):
    with open('debug-summary-completion.choices.txt', 'a') as f:
        for choice in choices:
            f.write("DEBUG CHOICE::" + choice.text.strip() + os.linesep)


def get_summary(response, temperature=0.5):
    prompt_text = clean_url_response2text(response)
    #print(prompt_text)
    completion = client.completions.create(
        model=model_to_use,
        prompt="You summarize the following text in 300 caracters: " + prompt_text,
        temperature=temperature,
    )
    write_to_debug_file(completion.choices)
    #return [choice.text.strip() for choice in completion.choices] if completion.choices else []
    return completion.choices[0].text.strip() if completion.choices else ""


def get_summary_diff(new_text, old_text, temperature=0.5):
    prompt_text = f"You tell me a summary of the changes between new and old text bellow : \n\n\nNEW TEXT: {new_text}\n\nOLD TEXT: {old_text}"
    completion = client.completions.create(
        model=model_to_use,
        prompt=prompt_text,
        temperature=temperature,
    )
    write_to_debug_file(completion.choices)
    return completion.choices[0].text.strip() if completion.choices else ""





# Load .env file from the current directory
load_dotenv()

# If the OPENAI_API_KEY is not found, try to load it from the .env file in the HOME directory
if 'OPENAI_API_KEY' not in os.environ:
    home_dir = os.path.expanduser("~")
    load_dotenv(os.path.join(home_dir, '.env'))
    
_api_key=os.getenv('OPENAI_API_KEY')


# Create directory if not exists
if not os.path.exists(f'{snote_cache_folder}'):
    os.makedirs(f'{snote_cache_folder}')


client = OpenAI(api_key=_api_key)


def main():
        
    # Load summaries and hashes of previously processed URLs, if the file exists
    try:
        print('Load summaries and hashes of previously processed URLs, if the file exists')
        with open('{snote_cache_folder}/data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        data = {}

    with open(snoter_datasource_csv, 'r') as csv_file:
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
            print('  Checking if hash changed :' + content_hash)
            
            if url not in data or data[url]['hash'] != content_hash:
                
                print( '             '+  content_hash +  ' ::    Not in content Hash')
                
                # Save the HTML content into a file
                save_html_content(url_hash, soup,title)
                
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
        with open(f'{snote_cache_folder}/data.json', 'w') as data_file:
            json.dump(data, data_file)
        

        # Call the function from snoterupdate.py
        #snoterupdate.generate_markdown(link_titles, data)


    from snoterupdate import generate_markdown
    #@STCStatus it runs it in the file when importing
    #generate_markdown()
        
        
    
if __name__ == "__main__":
    main()