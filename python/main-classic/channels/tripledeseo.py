# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tripledeseo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import sys
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item


def mainlist(item):
    logger.info("pelisalacarta.channels.tripledeseo mainlist")

    itemlist = []
    itemlist.append( Item(channel=item.channel, title="Peliculas" , action="peliculas" , url="http://www.tripledeseo.com/enlaces", viewmode="movie_with_plot"))
    return itemlist
 
 
def peliculas(item):
    logger.info("pelisalacarta.channels.tripledeseo peliculas")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    #data = scrapertools.find_single_match(data,'<div id="content">(.*?)</div><!-- #content -->')
    patron  = '<div class="ficha">(.*?)<div class="tipos">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'title="([^"]+)"')
        thumbnail = "http://www.tripledeseo.com/" + scrapertools.find_single_match(bloque,'<img src="([^"]+)"')
        url = "http://www.tripledeseo.com/" + scrapertools.find_single_match(bloque,'<a href="([^"]+)"')
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot="" , viewmode="movie_with_plot", folder=True) )
    
    # Extrae el paginador
    next_page = "http://www.tripledeseo.com/" + scrapertools.find_single_match(data,'<a href="([^"]+)" class="pagina pag_sig">')
    if next_page!="":
        itemlist.append( Item(channel=item.channel, action="peliculas", title=">> Pagina siguiente" , url=next_page , folder=True, viewmode="movie_with_plot") )
    
    return itemlist
