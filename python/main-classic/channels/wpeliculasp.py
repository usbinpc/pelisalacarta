# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para wpeliculasp
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
    logger.info("pelisalacarta.channels.wpeliculasp mainlist")

    itemlist = []
    itemlist.append( Item(channel=item.channel, title="Peliculas" , action="peliculas" , url="http://www.webpeliculasporno.com/", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Español" , action="peliculas" , url="http://www.webpeliculasporno.com/Categoria/espanol", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="HD" , action="peliculas" , url="http://www.webpeliculasporno.com/Categoria/en-hd", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Estrenos" , action="peliculas" , url="http://www.webpeliculasporno.com/Categoria/estrenos", viewmode="movie_with_plot"))
    return itemlist


 
def peliculas(item):
    logger.info("pelisalacarta.channels.wpeliculasp peliculas")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<div id="content">(.*?)</div><!-- #content -->')
    patron  = '<li class="border-radius-5 box-shadow">(.*?)</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'title="([^"]+)"')
        thumbnail = scrapertools.find_single_match(bloque,'<img width="180" height="257" src="([^<]+)" class="attachment-full size-full wp-post-image"')
        url = scrapertools.find_single_match(bloque,'<a href="([^"]+)"')
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot="" , viewmode="movie_with_plot", folder=True) )
    
    # Extrae el paginador
    next_page = scrapertools.find_single_match(data,'<a class="next page-numbers" href="([^"]+)"')
    if next_page!="":
        itemlist.append( Item(channel=item.channel, action="peliculas", title=">> Pagina siguiente" , url=next_page , folder=True, viewmode="movie_with_plot") )
    
    return itemlist
