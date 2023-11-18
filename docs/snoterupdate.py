import hashlib
import json

from bs4 import BeautifulSoup


def generate_markdown(data_file_path='./_snote_content_cache/data.json'):
    # Load summaries and hashes of previously processed URLs, if the file exists
    try:
        with open(data_file_path, 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        print("FileNotFoundError: [Errno 2] No such file or directory: './_snote_content_cache/data.json'")
        return

    # Create a list of tuples (link, title) from the data
    link_titles = [(url, info.get('title', url)) for url, info in data.items()]

    # Create index-snote.md

    with open('index-snote.md', 'w') as md_file:
        for link, title in link_titles:
            url_hash = hashlib.md5(link.encode()).hexdigest()
            summary = data[link]['summary'] if link in data else ''
            changes = data[link]['changes'] if link in data else ''

            # Parse and clean up the summary and changes with BeautifulSoup
            summary = BeautifulSoup(str(summary), 'html.parser').get_text(separator=' ')
            changes = BeautifulSoup(changes, 'html.parser').get_text(separator=' ')

            # # Replace problematic markdown characters
            # summary = summary.replace("`", "'").replace("```", "'")
            # changes = changes.replace("`", "'").replace("```", "'")

            md_file.write(f'# [{title}](./_snote_content_cache/{url_hash}.html) [ori]({link})\n')
            
            md_file.write(f'## Summary\n')
            md_file.write(f'{summary}\n')
            
            if changes:
                md_file.write(f'### Changes\n')
                md_file.write(f'{changes}\n\n')
            md_file.write(f'\n----\n\n----\n\n')
    print('Markdown file generated successfully.')

# Call the function
generate_markdown()