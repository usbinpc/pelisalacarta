# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para SeriesXD
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import sys
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item


DEBUG = config.get_setting("debug")


def mainlist(item):
    logger.info("pelisalacarta.channels.seriesxd mainlist")
    itemlist = []
    return series_genero(item)
 
 
def series(item):
    logger.info("pelisalacarta.channels.seriesxd series")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    patron  = '<li class="item">(.*?)</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'title="([^"]+)"')
        thumbnail = scrapertools.find_single_match(bloque,'<img src="([^"]+)"')
        url = scrapertools.find_single_match(bloque,'<a href="([^"]+)"')
        itemlist.append( Item(channel=item.channel, action="capitulos", title=title , url=url , thumbnail=thumbnail , plot="" , viewmode="movie_with_plot", folder=True) )
    
    # Extrae el paginador
    next = ""
    next_page = scrapertools.find_single_match(data,'<div class="pagination ">(.*?)</div>')
    pages = re.compile('<a href="([^"]+)"',re.DOTALL).findall(next_page)
    for page in pages:
        next = page
    if next!="":
        itemlist.append( Item(channel=item.channel, action="series", title="[COLOR blue]Pagina siguiente >>[/COLOR]", url=next, folder=True, viewmode="movie_with_plot") )
    
    return itemlist


def series_genero(item):
    logger.info("pelisalacarta.channels.seriesxd series_genero")
    itemlist = []
    
    data = scrapertools.cache_page("http://www.seriesxd.tv")
    data = scrapertools.find_single_match(data,'<div class="sub_title">Géneros</div>(.*?)<div class="col-md-80 lado2">')
    patron  = '<li>(.*?)</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'<i>([^<]+)</i>')
        url = scrapertools.find_single_match(bloque,'<a href="([^"]+)">')
        itemlist.append( Item(channel=item.channel, action="series", title=title , url=url , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    
    return itemlist


def capitulos(item):
    logger.info("pelisalacarta.channels.seriesxd capitulos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<div class="episode-guide">(.*?)<div class="col-md-4 padl0">')
    patron  = '<a h([^>]+)>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'title="([^"]+)"')
        url = scrapertools.find_single_match(bloque,'ref="([^"]+)"')
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title , url=url , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    
    return itemlist
