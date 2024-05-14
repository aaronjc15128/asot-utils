import requests
from bs4 import BeautifulSoup
import webbrowser
import os

def getTracklist(episode_number):
    episode_number = str(episode_number).strip()
    url = f'https://miroppb.com/ASOT/{episode_number}'
    response = requests.get(url)
    html = response.text
    tracklist_html = str(BeautifulSoup(html, 'html.parser').find(id='tracklist'))

    with open('temp.html', 'w', encoding='utf-8') as file:
        file.write(tracklist_html)

    absolute_path = os.path.abspath('temp.html')

    webbrowser.open(f'file://{absolute_path}')

    return 'Successful'

def getDownload(episode_number):
    episode_number = str(episode_number).strip()
    if len(episode_number) == 1: episode_number = f'00{episode_number}'
    elif len(episode_number) == 2: episode_number = f'0{episode_number}'

    response = requests.get(f'http://71.29.110.134:9995/asot/ASOT_Ep_{episode_number}.mp3', stream=True)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open a file in binary write mode
        with open(f'ASOT_Ep_{episode_number}', 'wb') as file:
            # Write the contents of the response to the file
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return f"File downloaded successfully as 'ASOT_Ep_{episode_number}'"
    else:
        return f"Failed to download file. Status code: {response.status_code}"


epinum = input("Episode # : ")
print("sending tracklist request")
print(getTracklist(epinum))
print("finished tracklist request")
print("sending download request")
print(getDownload(epinum))
print("finished download request")