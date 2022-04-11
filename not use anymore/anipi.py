import requests
import nextcord


color = 0xFFA500

def query(search, typeIS):
    query = '''
    query ($search: String! $type: MediaType!) { 
      Media (search: $search type: $type) { 
        id
        title {
          romaji
          english
        }
        status
        description
        averageScore
        startDate {
            year
            month
            day
        }
        endDate {
            year
            month
            day
        }
        coverImage {
          large  
        }
        genres
        siteUrl
        episodes
        chapters
        volumes
      }
    }
    '''
    variables = {
        'search' : search,
        'type' : typeIS,
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()

def get_anime(search):
    ani = query(search, 'ANIME')
    media = ani['data']['Media']

    if media is None:
      em = nextcord.Embed(title="No results found", description="Try again with a different search term.", color=color)
      return em
    else:

        # anime_id = media['id']
        url = media['siteUrl']
        title_romaji = media['title']['romaji']
        title_english = media['title']['english']
        averageScore = int(media['averageScore'])/10


        yearStart = media['startDate']['year']
        monthStart = media['startDate']['month']
        dayStart = media['startDate']['day']
        startDate = str(monthStart) + "/" + str(dayStart) + "/" + str(yearStart)

        yearEnd = media['endDate']['year']
        monthEnd = media['endDate']['month']
        dayEnd = media['endDate']['day']
        endDate = str(monthEnd) + "/" + str(dayEnd) + "/" + str(yearEnd)


        episodes = media['episodes']
        if episodes is None:
            episodes = "N/A"

        if endDate.startswith("None"):
            endDate = "N/A"
        if startDate.startswith("None"):
            startDate = "N/A"


        coverImage = media['coverImage']['large']
        genres = media['genres']

        description = media['description']

        for i in (('<br>',''), ('<i>', ''), ('</i>', ''), ('<br/>', '')):
          description = description.replace(*i)

        if len(description) > 800:
          description = description[:800] + "..."

        genres = ", ".join(genres)

        em = nextcord.Embed(title=f"{title_english} : ({url})",color=0x00ff00)
        em.add_field(name="Romaji Title", value= title_romaji, inline=True)
        em.add_field(name="Episodes", value= episodes, inline=True)
        em.add_field(name="Average Score", value=averageScore, inline=True)
        em.add_field(name="Start Date", value=startDate, inline=True)
        em.add_field(name="End Date", value=endDate, inline=True)
        em.add_field(name="Genres", value=genres, inline=True)
        em.add_field(name="Description", value=description, inline=False)
        em.set_thumbnail(url=coverImage)

        return em

def get_manga(search):
    ani = query(search, 'MANGA')
    media = ani['data']['Media']

    if media is None:
      em = nextcord.Embed(title="No results found", description="Try again with a different search term.", color=color)
      return em
    else:

        # anime_id = media['id']
        url = media['siteUrl']
        title_romaji = media['title']['romaji']
        title_english = media['title']['english']
        averageScore = int(media['averageScore'])/10


        yearStart = media['startDate']['year']
        monthStart = media['startDate']['month']
        dayStart = media['startDate']['day']
        startDate = str(monthStart) + "/" + str(dayStart) + "/" + str(yearStart)

        yearEnd = media['endDate']['year']
        monthEnd = media['endDate']['month']
        dayEnd = media['endDate']['day']
        endDate = str(monthEnd) + "/" + str(dayEnd) + "/" + str(yearEnd)


        volumes = media['volumes']
        chapters = media['chapters']

        if volumes is None:
            volumes = "N/A"
        if chapters is None:
            chapters = "N/A"

        if endDate.startswith("None"):
            endDate = "N/A"
        if startDate.startswith("None"):
            startDate = "N/A"

        coverImage = media['coverImage']['large']
        genres = media['genres']

        description = media['description']

        for i in (('<br>',''), ('<i>', ''), ('</i>', ''), ('<br/>', '')):
          description = description.replace(*i)

        if len(description) > 800:
          description = description[:800] + "..."

        genres = ", ".join(genres)

        em = nextcord.Embed(title=f"{title_english} : ({url})", color=color)
        em.add_field(name="Romaji Title", value= title_romaji, inline=True)
        em.add_field(name="Volumes", value= volumes, inline=True)
        em.add_field(name="Chapters", value=chapters, inline=True)
        em.add_field(name="Average Score", value=averageScore, inline=True)
        em.add_field(name="Start Date", value=startDate, inline=True)
        em.add_field(name="End Date", value=endDate, inline=True)
        em.add_field(name="Genres", value=genres, inline=True)
        em.add_field(name="Description", value=description, inline=False)
        em.set_thumbnail(url=coverImage)

        return em

def userSearch(name):
    query = '''
    query ($search: String!) { 
      User(search: $search){
        name
        avatar {
          large
        }
        about
        siteUrl
        favourites{
          anime {
            nodes{
              title {
                english
              }
            }
          }
          manga{
            nodes{
              title{
                english
              }
            }
          }
        }
      }
    }
    '''
    variables = {
        'search' : name,
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()

def get_user(name):
    data = userSearch(name)
    user = data['data']['User']
    if user is None:
      em = nextcord.Embed(title="No results found", description="Try again with a different search term.", color=color)
      return em
    else:
      uname = user['name']
      about = user['about']
      avatar = user['avatar']['large']
      siteUrl = user['siteUrl']
      favAnime = user['favourites'] # datatype is a dict
      favManga = user['favourites']
      
      animefav = []
      mangafav = []

      for i in range(len(favAnime['anime']['nodes'])):
        animefav.append(str(favAnime['anime']['nodes'][i]['title']['english']))

      for i in range(len(favManga['manga']['nodes'])):
        mangafav.append(str(favManga['manga']['nodes'][i]['title']['english']))

      anifav = ", ".join(animefav)
      manfav = ", ".join(mangafav)

      em = nextcord.Embed(title=f"{uname}'s Profile : ({siteUrl})", description=about, color=color)
      em.add_field(name=f"Anime Favorite (Entries : {len(animefav)})", value= anifav, inline=False)
      em.add_field(name=f"Manga Favorite (Entries : {len(mangafav)})", value= manfav, inline=False)
      em.set_thumbnail(url=avatar)

      return em