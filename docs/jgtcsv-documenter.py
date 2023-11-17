import os
import pandas as pd

def csv_to_markdown(csv_filepath):
  # reading csv file
  df = pd.read_csv(csv_filepath, delimiter=';')
  
  # replace NaN values with empty string
  df.fillna('', inplace=True)
  
  # converting the dataframe to markdown
  markdown_table = df.to_markdown(index=False)

  # appending the note
  markdown_table += "\n\n----\n\n----\n\nAutomatically generated - Please Edit the CSV File"

  # writing the markdown to a file
  md_filepath = csv_filepath.replace('.csv', '.md')
  with open(md_filepath, 'w') as md_file:
    md_file.write(markdown_table)



def convert_csv_to_markdown(filename):
  script_dir = os.path.dirname(os.path.realpath(__file__))
  input_file = os.path.join(script_dir, filename)
  csv_to_markdown(input_file)


convert_csv_to_markdown('indicators.csv')
convert_csv_to_markdown('signals.csv')