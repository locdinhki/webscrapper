import os
import re
import sys
import requests
import text_cleaner as tc
from bs4 import BeautifulSoup


def scrape_site():
    source_file_path = './source.txt'
    download_folder_path = './download/'

    with open(source_file_path, 'r') as f:
        sources = f.readlines()

    i = 0
    while i < len(sources):
        line = sources[i].replace('\n','')
        if line == '':
            i += 1
            continue
        title = line.split("|", 1)[0]
        URL = line.split("|", 1)[1]

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find and extract the text
        # results = soup.find(id='content')
        job_elem = soup.find('div', class_='entry-content')
        content_text = []
        try:
            content_text = job_elem.text.strip().split("\n")
        except:
            print("Can't find text")
            # Next index
            i += 1
            continue

        print(URL)
        
        # Clean up the text
        new_content_text = tc.clean(content_text)

        if len(new_content_text) > 0:
            
            chapter_title = new_content_text[0].replace('?', ' ').replace('!', ' ').strip()

            # Set current full title
            volume_title = ""
            try:
                volume_title = soup.find('h1', class_='entry-title').text.replace(title,'')
            except:
                pass
            full_title =''
            if volume_title != '' and ('vol' in volume_title or 'Vol' in volume_title):
                volume_number = [int(i) for i in volume_title.split() if i.isdigit()][0]
                full_title = title + " Volume " + str(volume_number)  + " " + chapter_title
            else:
                full_title = title + " " + chapter_title
            # Prepare save file
            output_folder = download_folder_path + title + "/"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            save_file = output_folder + full_title + ".txt"
            #cleaned_content = tc.clean(new_content_text)

            with open(save_file, "w", encoding='utf-8') as f:
                for a in new_content_text:
                    f.write(a+'\n')
        else:
            pass
        # Find the next URL
        next_URL = ''
        try:
            elements = soup.find('a', text=re.compile(".*ext.*"))
            next_URL = elements['href']
        except:
            print("Can't find next URL")
            # Next index
            i += 1
            continue

        # Update source data
        sources[i] = title + "|" + next_URL

        # Update source file
        with open(source_file_path, "w", encoding='utf-8') as f:
            f.seek(0)
            for a in sources:
                f.write(a+'\n')
            f.truncate()

    if i == len(sources):
        return -1

def string_decode(x):
    return x.decode("utf-8")
