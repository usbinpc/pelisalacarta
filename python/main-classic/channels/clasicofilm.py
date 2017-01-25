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
from core import jsontools
from core.item import Item


DEBUG = config.get_setting("debug")


def mainlist(item):
    logger.info("pelisalacarta.channels.clasicofilm mainlist")
    
    itemlist = []
    url = "http://www.clasicofilm.com/2016/01/prueba-2.html"
    data = scrapertools.cache_page(url)
    patron = '<script src="([^"]+)"></script><br/>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'-/([^?]+)?').upper()
        url = scrapertools.find_single_match(bloque,'(.*?)&callback=recentpostslist').replace(" ", "%20")
        itemlist.append( Item(channel=item.channel, action="peliculas_lista", title=title, url=url , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    
    return itemlist


def search(item,texto):
    logger.info("pelisalacarta.channels.pelisplanet search")
    try:
        return buscar(item,texto)
    # Se captura la excepci?n, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []


def buscar(item, texto=""):
    return itemlist


def peliculas_lista(item):
    logger.info("pelisalacarta.channels.clasicofilm peliculas_lista")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = data[28:len(data)-2]
    json_object = jsontools.load_json(data)
    for row in json_object['feed']['entry']:
        link = row['link'][4]['href']
        itemlist.append( Item(channel=item.channel, action="findvideos", title=row['title']['$t'] , url=link , thumbnail=row['media$thumbnail']['url'] , plot="" , viewmode="movie_with_plot", folder=True) )
    
    return itemlist


