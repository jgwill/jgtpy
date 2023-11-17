import hashlib
import json

def generate_markdown():
    # Load summaries and hashes of previously processed URLs, if the file exists
    try:
        with open('./_snote_content_cache/data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        print("FileNotFoundError: [Errno 2] No such file or directory: './_snote_content_cache/data.json'")
        return

    # Create a list of tuples (link, title) from the data
    link_titles = [(url, info.get('title', url)) for url, info in data.items()]

    # Create index-snote.md
    with open('index-snote.md', 'w') as md_file:
        md_file.write('| Title | Summary | Changes |\n')
        md_file.write('|-------|---------|---------|\n')
        for link, title in link_titles:
            url_hash = hashlib.md5(link.encode()).hexdigest()
            summary = data[link]['summary'] if link in data else ''
            changes = data[link]['changes'] if link in data else ''
            md_file.write(f'| [{title}](./_snote_content_cache/{url_hash}.html) | {summary} | {changes} |\n')

    print('Markdown file generated successfully.')

# Call the function
generate_markdown()