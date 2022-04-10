from selenium import webdriver
import time
import bs4
import nextcord
import pandas as pd
# from selenium.webdriver.chrome.options import Options


def embed_msg(desc):
    embed = nextcord.Embed(title="Ritsu Helper", description=desc)
    return embed


def driver(username, typeData, mode):
    # for replit Only

    # chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(options=chrome_options)

    driver = webdriver.Edge()
    if typeData == 'anime':
        if mode == 'all':
            url = f'https://anilist.co/user/{username}/animelist'
        elif mode == 'watching':
            url = f'https://anilist.co/user/{username}/animelist/Watching'
        elif mode == 'completed':
            url = f'https://anilist.co/user/{username}/animelist/Completed'
        elif mode == 'paused':
            url = f'https://anilist.co/user/{username}/animelist/Paused'
        elif mode == 'dropped':
            url = f'https://anilist.co/user/{username}/animelist/Dropped'
        elif mode == 'planning':
            url = f'https://anilist.co/user/{username}/animelist/Planning'
    elif typeData == 'manga':
        if mode == 'all':
            url = f'https://anilist.co/user/{username}/mangalist'
        elif mode == 'reading':
            url = f'https://anilist.co/user/{username}/mangalist/Reading'
        elif mode == 'completed':
            url = f'https://anilist.co/user/{username}/mangalist/Completed'
        elif mode == 'paused':
            url = f'https://anilist.co/user/{username}/mangalist/Paused'
        elif mode == 'planning':
            url = f'https://anilist.co/user/{username}/mangalist/Planning'

    driver.get(url)
    time.sleep(5)
    # scroll down
    # for i in range(3):
    #     driver.execute_script("window.scrollBy(0, 1000)")
    #     time.sleep(1)

    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')

    return soup


def findTitle(soup):
    title_list = []
    for c in soup.find_all('div', {'class': 'title'}):
        c = c.text.replace("\n", "").replace("\t", "").replace("  ", "")
        if not c.startswith("Title"):
            title_list.append(c)
    return title_list


def findScore(soup):
    score_list = []
    for c in soup.find_all('div', {'class': 'score'}):
        c = c.text.replace("\n", "").replace("\t", "")
        if len(c) > 0 and not c.startswith("Score"):
            score_list.append(c)
        elif len(c) == 0:
            score_list.append("N/A")
    return score_list


def findProgress(soup):
    progress_list = []
    for c in soup.find_all('div', {'class': 'progress'}):
        c = c.text.replace("\n", "").replace("\t", "").replace("+", "")
        if len(c) > 0 and not c.startswith("Progress") and not c.startswith("Chapters") and not c.startswith("Volumes"):
            progress_list.append(c)
    return progress_list


def findName(soup):
    name = soup.find('h1', {'class': 'name'})
    name = name.text.replace("\n", "").replace("\t", "").replace("  ", "")
    return name


def ani_search(username: str, typeData: str, mode: str):
    msg = ''
    soup = driver(username, typeData, mode)
    title = findTitle(soup)
    score = findScore(soup)
    name = findName(soup)
    progress = findProgress(soup)
    for i in range(len(title)):
        if i < 24:
            if len(msg) < 4000:
                # msg += f'{i+1}. [{progress_list[i]}]{title_list[i]}  : {score_list[i]}\n'
                msg += f'[`{progress[i]}`]{title[i]}\n'
        else:
            msg += f'[`{progress[i]}`]{title[i]} ....'
            break


    table = pd.DataFrame([title, score, progress]).transpose()
    table.columns = ['Title', 'Score', 'Progress']
    table.to_csv('animelist.csv', index=False)
    
    em = nextcord.Embed(
        title=f'**{name}** : `{len(title)}` entries found.', description=msg)
    return em
