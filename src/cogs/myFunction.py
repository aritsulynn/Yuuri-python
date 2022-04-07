import time
import nextcord
import bs4
from numpy import mat
from selenium import webdriver


def embed_msg(desc):
    embed = nextcord.Embed(title="Ritsu Helper", description=desc)
    return embed

def ani_search(username, mode):
    match mode:
        case "all": 
            url = f'https://anilist.co/user/{username}/animelist'
        case "watching":
            url = f'https://anilist.co/user/{username}/animelist/Watching'
        case "completed":
            url = f'https://anilist.co/user/{username}/animelist/Completed'

    # url = f'https://anilist.co/user/{username}/animelist/'
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(5)
    driver.find_element_by_xpath(f'//*[@id="{username}"]/div[2]/div[1]/div/span[1]').click()

    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    title_list = []
    score_list = []
    all_dict = {}
    msg = ""

    for c in soup.find_all('div', {'class': 'entry row'}):
        title_list.append(getattr(c.find('a'), 'text', None))
        score_list.append(getattr(c.find('div', {'class': 'score'}), 'text', None))

    for i,j in zip(title_list, score_list):
        i = i.replace("\n", "").replace("\t", "")
        j = j.replace("\n", "").replace("\t", "")
        all_dict[i] = j if(len(j) >= 1) else "N/A"


    for k, v in all_dict.items():
        if(len(msg) <= 500):
            msg += f"`{k}` - `{v}`\n"
        else:
            msg += "..."
            break
    return embed_msg(msg)