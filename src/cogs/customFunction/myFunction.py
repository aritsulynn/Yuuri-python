import time
import nextcord
import bs4
from numpy import mat
from selenium import webdriver


def embed_msg(desc):
    embed = nextcord.Embed(title="Ritsu Helper", description=desc)
    return embed
