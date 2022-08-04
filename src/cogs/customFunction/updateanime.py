from datetime import datetime
from tabnanny import check
import requests
from bs4 import BeautifulSoup
from os.path import exists as file_exists

# prototype code

def get_data():
    responses = requests.get('https://www.animenewsnetwork.com/encyclopedia/reports.xml?id=148&nlist=15')
    soup = BeautifulSoup(responses.text , "html.parser")
    dataAnimeAll = []
    for soup in soup.find_all('anime'):
        dataAnimeAll.append(soup.text + "\n")
    return dataAnimeAll


def write_test(dataAnimeAll):
    
    try:
        with (open('anime/data.txt', 'w', encoding="utf-8") as data,
         open('anime/name_checking.txt', 'r+', encoding="utf-8") as name_checking):
        # check last anime name
            anime_name = name_checking.readline()
            # print(anime_name.split('/n')[0] == dataAnimeAll[0].split('/n')[0])
            
            # if anime_name != dataAnimeAll[0]:
            for i in dataAnimeAll:
                if i.split("\n")[0] != anime_name.split("\n")[0]:
                    # print(i)
                    data.write(i)
                else:
                    # print("Updated")     
                    break
            name_checking.seek(0)
            name_checking.truncate()
            name_checking.write(dataAnimeAll[0])
            # else:
            #     print("No update found")

    except IOError:
        # One-time
        with open('anime/data.txt', 'w', encoding="utf-8") as data, open('anime/name_checking.txt', 'w', encoding="utf-8") as name_checking:
            data.write(''.join(dataAnimeAll))
            name_checking.write(dataAnimeAll[0])

            name_checking.close()
            data.close()
        print("[One-time]Data written to file")

def check_update_or_not():
    try:
        with open("anime/name_checking.txt", "r", encoding="utf-8") as f:
            last_anime_name = f.readline()
            print(get_data()[0].split('\n')[0] == last_anime_name.split('\n')[0])
            if last_anime_name.split('\n')[0] != get_data()[0].split('\n')[0]:
                print("Updated!")
                write_test(get_data())
                return True
            else:
                print("No update found!")
                return False
    except IOError:
        write_test(get_data())

def send_update():
    all_names = []
    with open("anime/data.txt", "r", encoding="utf-8") as f:
        for i in f.readlines():
            all_names.append(i)
        f.close()
    return all_names

# write_test(get_data())
# check_update_or_not()

# print(send_update())