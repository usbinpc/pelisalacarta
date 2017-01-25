# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelis24
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
    logger.info("pelisalacarta.channels.cine-tube mainlist")
    return generos(item, "http://www.cine-tube.com")


def generos(item, url):
    itemlist = []
    # estrenos
    itemlist.append( Item(channel=item.channel, action="listado", title="Novedades", url="http://www.cine-tube.com/?page=1" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    # generos
    data = scrapertools.cache_page(url)
    data = scrapertools.find_single_match(data, '<div class="categorias">(.*?)</div>')
    patron  = '<a title=(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'<strong>([^<]+)</strong>')
        dir = scrapertools.find_single_match(bloque,'ref="([^"]+)"')
        itemlist.append( Item(channel=item.channel, action="listado", title=title, url=dir+"?page=1" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
        
    return itemlist


def listado(item):
    itemlist = []
    data = scrapertools.cache_page(item.url)
    patron  = '<div class="box-poster">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'<span>([^<]+)</span>')
        img = scrapertools.find_single_match(bloque,'img src="([^"]+)"')
        url = scrapertools.find_single_match(bloque,'href="([^"]+)"')
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title, url=url , thumbnail=img , plot="" , viewmode="movie_with_plot", folder=True) )
    
    # pagina siguiente
    adr = item.url.replace("?", "'") + "'"
    act = scrapertools.find_single_match(adr,"=([^']+)'")
    next = item.url[0:(item.url).find("=")] + "=" + str(int(act)+1)
    
    itemlist.append( Item(channel=item.channel, action="listado", title="[COLOR blue]Siguiente pagina >>[/COLOR]", url=next , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    
    return itemlist

