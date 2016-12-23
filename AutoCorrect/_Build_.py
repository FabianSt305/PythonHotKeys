import requests
from bs4 import BeautifulSoup
import re

url = "https://en.wikipedia.org/wiki/Commonly_misspelled_English_words"
r = requests.get(url)

soup = BeautifulSoup(r.content,
                     "html.parser")

with open('AutoCorrect.py', 'w') as python_file:
    python_file.write("import keyboard\n\n\n")
    for list_item in soup.find_all('li'):
        item_text = list_item.text
        item_text_list = item_text.split("[")
        if len(item_text_list) > 1:
            correct, misspellings = item_text_list[0].split(u' \u2013 ')
            c = correct.split("/")[0]
            misspellings_list = misspellings.split(", ")
            for misspelling in misspellings_list:
                m = misspelling.split("(")[0]
                python_file.write('keyboard.add_abbreviation("%s", "%s ")\n' % (m, c))
