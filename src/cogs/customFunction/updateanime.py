from datetime import datetime
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

# one time code
def write_data(dataAnimeAll):

    if file_exists("last_anime_name.txt") and ("data.txt"):
        # check last anime name
        with open("last_anime_name.txt", "r+", encoding="utf-8") as old_data:
                last_anime_name = old_data.readline()  
                old_data.write(dataAnimeAll[0])
                old_data.close()

        with open("data.txt", "w", encoding="utf-8") as f:
                for i in dataAnimeAll:
                    if i.split("\n")[0] != last_anime_name.split("\n")[0]:
                        f.write(i.split("\n")[0] + "\n")
                    else: 
                        break
        f.close()
        print("Data updated")

    elif not file_exists("last_anime_name.txt") or not file_exists("data.txt"):
        with open("data.txt", "w", encoding="utf-8") as new_data:
                new_data.write(''.join(dataAnimeAll))
                new_data.close()
        with open("last_anime_name.txt", "w", encoding="utf-8") as old_data:
                old_data.write(dataAnimeAll[0])
                old_data.close()
                
        print("[One-time]Data written to file")

    # update last anime name
        with open("last_anime_name.txt", "w", encoding="utf-8") as f:
            f.write(dataAnimeAll[0])
            f.close()

def check_update_or_not():
    if file_exists("last_anime_name.txt") and file_exists("data.txt"):
        with open("last_anime_name.txt", "r", encoding="utf-8") as f:
            last_anime_name = f.readline()
            f.close()
        with open("data.txt", "r", encoding="utf-8") as f:
            data = f.readlines()
            f.close()
        if last_anime_name.split("\n")[0] != data[0].split("\n")[0]:
            write_data(get_data())
            print("Updated")
            return True
        else:
            time = datetime.now().strftime("%H:%M:%S")
            print(f"{time} has no update" )
            return False
    else:
        print("File does not exist and already created new file")
        write_data(get_data())
        return True

def send_update():
    all_names = []
    with open("data.txt", "r", encoding="utf-8") as f:
        for i in f.readlines():
            all_names.append(i)
        f.close()
    return all_names

