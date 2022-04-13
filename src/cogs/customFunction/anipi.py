import nextcord
import anipie

color = 0xFFA500


def get_anime(search):
    ani = anipie.SearchAnime(search)

    try:
        title_english = ani.getAnimeEnglishName()
        title_romaji = ani.getAnimeRomajiName()
        url = ani.getAnimeSiteUrl()
        coverImage = ani.getAnimeCoverImage()
        description = ani.getAnimeDescription()
        startDate = ani.getAnimeStartDate()
        endDate = ani.getAnimeEndDate()
        averageScore = ani.getAnimeAverageScore()
        genres = ani.getAnimeGenres()
        episodes = ani.getAnimeEpisodes()
        animeID = ani.getAnimeID()

        if len(description) > 800:
            description = description[:800] + "..."

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
    except:
        em = nextcord.Embed(title="No results found", description="Try again with a different search term.", color=color)
        return em

def get_manga(search):
    manga = anipie.SearchManga(search)

    try:
        title_english = manga.getMangaEnglishName()
        title_romaji = manga.getMangaRomajiName()
        url = manga.getMangaSiteUrl()
        coverImage = manga.getMangaCoverImage()
        description = manga.getMangaDescription()
        startDate = manga.getMangaStartDate()
        endDate = manga.getMangaEndDate()
        averageScore = manga.getMangaAverageScore()
        genres = manga.getMangaGenres()
        chapters = manga.getMangaChapters()
        volumes = manga.getMangaVolumes()
        status = manga.getMangaStatus()
        mangaID = manga.getMangaID()
        
        if len(description) > 800:
            description = description[:800] + "..."
      
        em = nextcord.Embed(title=f"{title_english} : ({url})", color=color)
        em.add_field(name="Romaji Title", value= title_romaji, inline=True)
        em.add_field(name="Volumes", value= volumes, inline=True)
        em.add_field(name="Chapters", value=chapters, inline=True)
        em.add_field(name="Average Score", value=averageScore, inline=True)
        em.add_field(name="Status", value=status, inline=True)
        em.add_field(name="Start Date", value=startDate, inline=True)
        em.add_field(name="End Date", value=endDate, inline=True)
        em.add_field(name="Genres", value=genres, inline=True)
        em.add_field(name="Description", value=description, inline=False)
        em.set_thumbnail(url=coverImage)

        return em
    except:
        em = nextcord.Embed(title="No results found", description="Try again with a different search term.", color=color)
        return em

def get_user(name):
      user = anipie.SearchUser(name)  

      try:
          uname = user.getUserName()
          url = user.getUserSiteUrl()
          avatar = user.getUserAvatar()
          about = user.getUserAbout()
          anifav = user.getUserFavouritesAnime()
          manfav = user.getUserFavouritesManga()
          animeEntries = user.getUserEntriesFavAnime()
          mangaEntries = user.getUserEntriesFavManga()

          em = nextcord.Embed(title=f"{uname}'s Profile : ({url})", description=about, color=color)
          em.add_field(name=f"Anime Favorite (Entries : {animeEntries})", value= anifav, inline=False)
          em.add_field(name=f"Manga Favorite (Entries : {mangaEntries})", value= manfav, inline=False)
          em.set_thumbnail(url=avatar)
          return em
      except:
          em = nextcord.Embed(title="No results found", description="Try again with a different search term.", color=color)
          return em