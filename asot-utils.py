import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import sys
from mutagen.mp3 import MP3
import datetime

def timestamps(episode_number, repetitions):
    i = 0
    for _ in range(int(repetitions)):
        download(episode_number, 1)

        epinum = int(str(episode_number).strip()) + i
        if len(str(epinum)) == 1: epinum = f'00{epinum}'
        elif len(str(epinum)) == 2: epinum = f'0{epinum}'

        audiofile = MP3(f"ASOT_Ep_{epinum}.mp3")
        length = audiofile.info.length

        epinum = int(str(episode_number).strip()) + i
        url = f'https://miroppb.com/ASOT/{epinum}'
        response = requests.get(url)
        html = response.text
        tracklist_html = str(BeautifulSoup(html, 'html.parser').find(id='tracklist'))

        with open('asot-tracklist.html', 'w', encoding='utf-8') as file:
            file.write(tracklist_html)
        
        with open('asot-tracklist.html', 'r', encoding='utf-8') as file:
            trackcount = 0
            for line in file:
                if line[1:3] == 'li':
                    trackcount += 1

        timepertrack = length / trackcount

        stamps, running = [], 0
        for _ in range(trackcount):
            running += timepertrack
            stamps.append(running)

        timestamps = []
        for stamp in stamps:
            timestamps.append(str(datetime.timedelta(seconds=stamp)))

        j = 0
        while j < len(timestamps):
            timestamps[j] = timestamps[j][:7]
            j += 1

        epinum = int(str(episode_number).strip()) + i
        if len(str(epinum)) == 1: epinum = f'00{epinum}'
        elif len(str(epinum)) == 2: epinum = f'0{epinum}'

        with open('asot-tracklist.html', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        lines.insert(0, '<html style="background-color:#161616;color:white"><br>')
        lines.insert(2, f'<h3>A State of Trance {epinum}</h3>')
        lines.append('</html>')

        j, stampnum = 0, 0
        while j < len(lines):
            current = lines[j]
            if current[1:3] == 'li':
                lines[j] = f'{current[:4]}<span style="color:pink">{timestamps[stampnum]} ~ </span>{current[4:]}'
                stampnum += 1
            j += 1

        with open('asot-tracklist.html', 'w', encoding='utf-8') as file:
            lines = file.writelines(lines)

        absolute_path = os.path.abspath('asot-tracklist.html')
        webbrowser.open(f'file://{absolute_path}', new=1)

        if os.path.exists(os.path.abspath(f"ASOT_Ep_{epinum}.mp3")):
            os.remove(os.path.abspath(f"ASOT_Ep_{epinum}.mp3"))

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
        else:
            print(f'!! failed to download {epinum}')

        i += 1

if __name__ =="__main__":
    if len(sys.argv) != 4:
        print("usage: python asot-utils.py function episode_number repetitions")
        sys.exit(1)

    function = sys.argv[1]
    parameter = sys.argv[2]
    repetitions = sys.argv[3]

    try:
        (globals()[function])(parameter, repetitions) # runs function as function(parameter, repetitions)
    except:
        print("invalid!")

    input()

    if os.path.exists(os.path.abspath('asot-tracklist.html')):
        os.remove(os.path.abspath('asot-tracklist.html'))