# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para soloclasicas
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
    logger.info("pelisalacarta.channels.soloclasicas mainlist")
    
    itemlist = []
    #itemlist.append( Item(channel=item.channel, title="Comedias" , action="peliculas_1" , url="http://www.comediasclasicas.info/search?q=*", viewmode="movie_with_plot"))
    #itemlist.append( Item(channel=item.channel, title="Western" , action="peliculas_1" , url="http://www.solowestern.info/search?q=*", viewmode="movie_with_plot"))
    #itemlist.append( Item(channel=item.channel, title="Negro y policial" , action="peliculas_2" , url="http://www.cinenegroypolicial.info/search?q=*", viewmode="movie_with_plot"))
    #itemlist.append( Item(channel=item.channel, title="Belico" , action="peliculas_3" , url="http://www.cinebelico.info/search?q=*", viewmode="movie_with_plot"))
    
    itemlist.append( Item(channel=item.channel, title="Lista Comedias" , action="peliculas_lista" , url="http://www.comediasclasicas.info/p/peliculas.html", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Lista Aventuras" , action="peliculas_lista" , url="http://www.cinedeaventuras.info/p/peliculas.html", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Lista Western" , action="peliculas_lista" , url="http://www.solowestern.info/p/peliculas.html", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Lista Negro y Policial" , action="peliculas_lista" , url="http://www.cinenegroypolicial.info/p/peliculas.html", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Lista Belico" , action="peliculas_lista" , url="http://www.cinebelico.info/p/peliculas.html", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Lista Español" , action="peliculas_lista" , url="http://www.cineespanolclasico.info/p/indice-de-peliculas.html", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Lista Fantastico y Terror" , action="peliculas_lista" , url="http://www.cinefantasticoydeterror.info/p/peliculas.html", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Lista Clasicos Modernos" , action="peliculas_lista" , url="http://www.soloclasicosmodernosdecine.info/p/peliculas.html", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Lista Drama" , action="peliculas_lista" , url="http://www.dramasclasicos.info/p/peliculas.html", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Lista VOSE" , action="peliculas_lista" , url="http://www.solocineenvose.info/p/peliculas.html", viewmode="movie_with_plot"))
    
    return itemlist


# Blog de Comedias y Western
def peliculas_1(item):
    logger.info("pelisalacarta.channels.soloclasicas peliculas_1")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    patron  = "<div class='post_item'>(.*?)<div class='clear'>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,"title='([^<]+)'")
        thumbnail = scrapertools.find_single_match(bloque,'border="0" height="640" src="([^"]+)" title=')
        url = scrapertools.find_single_match(bloque,"<a href='([^']+)'")
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot="" , viewmode="movie_with_plot", folder=True) )
    
    # Extrae el paginador
    next_page = scrapertools.find_single_match(data,"<a class='blog-pager-older-link' href='([^']+)' id='Blog1_blog-pager-older-link'")
    if next_page!="":
        itemlist.append( Item(channel=item.channel, action="peliculas_1", title=">> Pagina siguiente" , url=next_page , folder=True, viewmode="movie_with_plot") )
    
    return itemlist

# Blog cine negro y policial
def peliculas_2(item):
    logger.info("pelisalacarta.channels.soloclasicas peliculas_2")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    patron  = "<div class='grid-item col-md-4'(.*?)<div style='clear: both;'>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,"html'>([^<]+)</a></h2>")
        thumbnail = scrapertools.find_single_match(bloque,"<a class='fancybox' href='([^']+)'><i class=")
        url = scrapertools.find_single_match(bloque,"<h2><a href='([^']+)'")
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot="" , viewmode="movie_with_plot", folder=True) )
    
    # Extrae el paginador
    next_page = scrapertools.find_single_match(data,"<a class='blog-pager-older-link' href='([^']+)' id='Blog1_blog-pager-older-link'")
    if next_page!="":
        itemlist.append( Item(channel=item.channel, action="peliculas_2", title=">> Pagina siguiente" , url=next_page , folder=True, viewmode="movie_with_plot") )
    
    return itemlist

# Blog cine belico
def peliculas_3(item):
    logger.info("pelisalacarta.channels.soloclasicas peliculas_3")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    patron  = '<div class="date-outer">(.*?)</article>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,"#more' title='([^']+)'>")
        thumbnail = scrapertools.find_single_match(bloque,"<meta content='([^']+)' itemprop=")
        url = scrapertools.find_single_match(bloque,"<a class='timestamp-link' href='([^']+)' rel='bookmark'")
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot="" , viewmode="movie_with_plot", folder=True) )
    
    # Extrae el paginador
    next_page = scrapertools.find_single_match(data,"<a class='blog-pager-older-link' href='([^']+)' id='Blog1_blog-pager-older-link'")
    if next_page!="":
        itemlist.append( Item(channel=item.channel, action="peliculas_3", title=">> Pagina siguiente" , url=next_page , folder=True, viewmode="movie_with_plot") )
    
    return itemlist


def peliculas_lista(item):
    logger.info("pelisalacarta.channels.soloclasicas peliculas_lista")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    #data = scrapertools.find_single_match(data,"<article class='post hentry' itemprop='blogPost' itemscope='itemscope' itemtype='http://schema.org/BlogPosting'>(.*?)</article>")
    patron  = '<a href="([^"]+)" target="_blank"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:
        year = scrapertools.find_single_match(bloque,"/([^/]+)",1).upper()
        title = scrapertools.find_single_match(bloque,"/([^/]+)",3).upper()
        title = scrapertools.find_single_match(title,"([^.]+)").replace("-", " ")
        url = bloque
        if year in ['2012','2013','2014','2015','2016','2017','2018']:
            if title:
                itemlist.append( Item(channel=item.channel, action="findvideos", title=title , url=url , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
        
    return itemlist


