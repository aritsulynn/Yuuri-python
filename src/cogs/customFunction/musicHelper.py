import nextcord
from datetime import datetime


color = 0xcc9410

# convert seconds to minutes and seconds
def convert_time(seconds):
    m, s = divmod(seconds, 60)
    return "%02d:%02d" % (m, s)

# controller embed for music
def controller(song_name, duration, uri, thumbnail):
    em = nextcord.Embed(title=song_name, color=color, timestamp=datetime.now(),
     description="[%s minutes](%s)" % (duration, uri))
    em.set_thumbnail(url=thumbnail)
    return em

# queue embed for music
def queue_list(song_name):
    em = nextcord.Embed(title="Queue List", color=color, timestamp=datetime.now(), description="\n".join(song_name))
    return em


def embed_msg(description):
    em = nextcord.Embed(title="Ritsu Helper:)", color=color, timestamp=datetime.now(), description=description)
    return em

