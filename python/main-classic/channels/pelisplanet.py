# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para PelisPlanet
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
    logger.info("pelisalacarta.channels.pelisplanet mainlist")

    itemlist = []
    itemlist.append( Item(channel=item.channel, title="Estrenos" , action="peliculas" , url="http://www.pelisplanet.com/genero/estrenos/", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Castellano" , action="peliculas" , url="http://www.pelisplanet.com/idioma/castellano/", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Generos" , action="peliculas_genero" , url="http://www.pelisplanet.com/generos/", viewmode="movie_with_plot"))
    return itemlist



 
def peliculas(item):
    logger.info("pelisalacarta.channels.pelisplanet peliculas")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    #data = scrapertools.find_single_match(data,'<div id="content-dark">(.*?)</div>')
    patron  = '<div class="browse-movie-wrap col-xs-10 col-sm-5">(.*?)</figure>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'<h2 class="info-title one-line">([^<]+)</h2>')
        thumbnail = scrapertools.find_single_match(bloque,'<img class="img-responsive" src="([^<]+)" alt=')
        url = scrapertools.find_single_match(bloque,'<a href="([^"]+)" class="browse-movie-link"')
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot="" , viewmode="movie_with_plot", folder=True) )
    
    # Extrae el paginador
    next_page = scrapertools.find_single_match(data,'<a class="nextpostslink" rel="next" href="([^"]+)">')
    if next_page!="":
        itemlist.append( Item(channel=item.channel, action="peliculas", title=">> Pagina siguiente" , url=next_page , folder=True, viewmode="movie_with_plot") )
    
    return itemlist


def peliculas_genero(item):
    logger.info("pelisalacarta.channels.pelisplanet peliculas_genero")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    patron  = '<div class="todos">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'title="([^<]+)">')
        thumbnail = scrapertools.find_single_match(bloque,'<img src="([^<]+)" alt=')
        url = scrapertools.find_single_match(bloque,'<a href="(.*?)" title')
        itemlist.append( Item(channel=item.channel, action="peliculas", title=title , url=url , thumbnail=thumbnail , plot="" , viewmode="movie_with_plot", folder=True) )
        
    return itemlist

