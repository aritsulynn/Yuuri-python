import requests
from bs4 import BeautifulSoup
from os.path import exists as file_exists

# prototype code

def get_data():
    data = requests.get('https://www.animenewsnetwork.com/encyclopedia/reports.xml?id=148&nlist=15')
    soup = BeautifulSoup(data.text , "html.parser")
    name_list = []
    for soup in soup.find_all('anime'):
        name_list.append(soup.text + "\n")
    return name_list


            
# one time code
def write_data(name_list):

    if not file_exists("data.txt") and not file_exists("last_anime_name.txt"):
        with (open("data.txt", "w", encoding="utf-8") as new_data,
             open("last_anime_name.txt", "w", encoding="utf-8") as old_data):
                new_data.write(''.join(name_list))
                old_data.write(name_list[0])
                
                new_data.close()
                old_data.close()
                
                print("[One-time]Data written to file")

    elif (file_exists("last_anime_name.txt") and ("data.txt") ):
        # check last anime name
        with open("last_anime_name.txt", "r+", encoding="utf-8") as old_data:
            last_anime_name = old_data.readline()  
            old_data.write(name_list[0])
            old_data.close()

        with open("data.txt", "w", encoding="utf-8") as f:
                for i in name_list:
                    if i != last_anime_name:
                        f.write(i.split("\n")[0] + "\n")
                    else: 
                        break
        f.close()
        print("Data updated")

        # update last anime name
        with open("last_anime_name.txt", "w", encoding="utf-8") as f:
            f.write(name_list[0])
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
            return True
        else:
            return False
    elif not file_exists("last_anime_name.txt") and not file_exists("data.txt"):
        write_data(get_data())
        return False

def send_update():
    all_names = []
    with open("data.txt", "r", encoding="utf-8") as f:
        for i in f.readlines():
            all_names.append(i)
        f.close()
    return all_names

# write_data(get_data())
# print(send_update())