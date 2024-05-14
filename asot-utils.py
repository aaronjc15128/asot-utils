import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import sys

def tracklist(episode_number, repetitions):
    i = 0
    for _ in range(int(repetitions)):
        epinum = int(str(episode_number).strip()) + i
        url = f'https://miroppb.com/ASOT/{epinum}'
        response = requests.get(url)
        html = response.text
        tracklist_html = str(BeautifulSoup(html, 'html.parser').find(id='tracklist'))

        with open('temp.html', 'w', encoding='utf-8') as file:
            file.write(tracklist_html)

        absolute_path = os.path.abspath('temp.html')
        webbrowser.open(f'file://{absolute_path}', new=1)

        print(f'successful {epinum}')

        i += 1

def download(episode_number, repetitions):
    i = 0
    for _ in range(int(repetitions)):
        epinum = int(str(episode_number).strip()) + i
        if len(str(epinum)) == 1: epinum = f'00{epinum}'
        elif len(str(epinum)) == 2: epinum = f'0{epinum}'

        response = requests.get(f'http://71.29.110.134:9995/asot/ASOT_Ep_{epinum}.mp3', stream=True)

        if response.status_code == 200:
            with open(f'ASOT_Ep_{epinum}.mp3', 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f'successful {epinum}')
        else:
            print(f'failed {epinum}')

        i += 1

if __name__ =="__main__":
    if len(sys.argv) != 4:
        print("usage: python asot-utils.py function episode_number repetitions")
        sys.exit(1)

    function = sys.argv[1]
    parameter = sys.argv[2]
    repetitions = sys.argv[3]

    #(globals()[function])(parameter, repetitions) # runs function as function(parameter, repetitions)

    try:
        (globals()[function])(parameter, repetitions) # runs function as function(parameter, repetitions)
    except:
        print("invalid!")

    input()