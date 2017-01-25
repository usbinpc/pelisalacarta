# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para RTVE
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
    logger.info("pelisalacarta.channels.rtve mainlist")
    itemlist = []
    itemlist.append( Item(channel=item.channel, action="catalogo", title="A la carta", url="http://www.rtve.es/alacarta/programlist.shtml?ctx=archivo&paginaBusqueda=1&category=tve&lang=es" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    itemlist.append( Item(channel=item.channel, action="listado", title="Series", url="http://www.rtve.es/alacarta/mod/programas/tve/series/1/?pageSize=40&order=1&criteria=asc&emissionFilter=all" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    itemlist.append( Item(channel=item.channel, action="listado", title="Documentales", url="http://www.rtve.es/alacarta/mod/programas/tve/documentales/1/?pageSize=40&order=1&criteria=asc&emissionFilter=all" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    itemlist.append( Item(channel=item.channel, action="listado", title="Ciencia", url="http://www.rtve.es/alacarta/mod/programas/tve/ciencia-y-tecnologia/1/?pageSize=40&order=1&criteria=asc&emissionFilter=all" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    itemlist.append( Item(channel=item.channel, action="listado", title="Música", url="http://www.rtve.es/alacarta/mod/programas/tve/musica/1/?pageSize=40&order=1&criteria=asc&emissionFilter=all" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    itemlist.append( Item(channel=item.channel, action="listado", title="Archivo", url="http://www.rtve.es/alacarta/mod/programas/tve/archivo/1/?pageSize=40&order=1&criteria=asc&emissionFilter=all" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    itemlist.append( Item(channel=item.channel, action="listado", title="Cultura", url="http://www.rtve.es/alacarta/mod/programas/tve/cultura/1/?pageSize=40&order=1&criteria=asc&emissionFilter=all" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    return itemlist


def catalogo(item):
    itemlist = []
    data = scrapertools.cache_page(item.url)
    patron  = '<dd>(.*?)</dd>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'title="([^"]+)"')
        url = scrapertools.find_single_match(bloque,'href="([^"]+)"')
        itemlist.append( Item(channel=item.channel, action="contenido", title=title, url=url , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    
    data = scrapertools.find_single_match(data, 'class="siguiente">(.*?)</li>')
    next = scrapertools.find_single_match(data, '<a name="paginaIR" href="([^"]+)"').replace("&amp;", "&").replace("?pbq=","?paginaBusqueda=")
    if next != "":
        itemlist.append( Item(channel=item.channel, action="catalogo", title="[COLOR blue]Siguiente pagina >>[/COLOR]", url="http://www.rtve.es/alacarta/programlist.shtml"+next , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    
    return itemlist


def contenido(item):
    itemlist = []
    # Calcular identificador de los contenidos
    data = scrapertools.cache_page(item.url)
    id = scrapertools.find_single_match(data, '<li class="favoritos" name="([^"]+)">')
    list = "http://www.rtve.es/alacarta/filterVideoSlide.shtml?ctx="+id+"&seasonFilter=-1"
        
    # Cargar lista de contenido
    data2 = scrapertools.cache_page(list)
    matches = re.compile('<li class="thumbox">(.*?)</li>', re.DOTALL).findall(data2)
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'<a title="([^"]+)"')
        img = scrapertools.find_single_match(bloque,'src="([^"]+)"')
        url = "http://www.rtve.es"+scrapertools.find_single_match(bloque,'<a href="([^"]+)"')
        itemlist.append( Item(channel=item.channel, action="episodio", title=title, url=url , thumbnail=img , plot="" , viewmode="movie_with_plot", folder=True) )
    
    return itemlist


def episodio(item):
    itemlist = []
    
    calc = "http://www.piraminetlab.com/enlaces.php?url_original="+item.url
    data = scrapertools.cache_page(calc)
    vid = scrapertools.find_single_match(data, '<INPUT TYPE="hidden" NAME="urls" VALUE="([^"]+)"')
    img = scrapertools.find_single_match(data, "<div id='imagen' style='background: #fff'><img src='([^']+)'")
    name = scrapertools.find_single_match(data, "<div id='info_titulo'>([^<]+)</div>")
    itemlist.append( Item(channel=item.channel, action="play", title="[COLOR yellow](VIDEO)[/COLOR] "+name, url=vid , thumbnail=img , plot="" , viewmode="movie_with_plot", folder=True) )
    return itemlist


def listado(item):
    itemlist = []
    data = scrapertools.cache_page(item.url)
    content = scrapertools.find_single_match(data, '<div class="ContentTabla">(.*?)<div class="pagbox mark">')
    
    matches = re.compile('<span class="col_tit" id="(.*?)</span>', re.DOTALL).findall(content)
    for bloque in matches:
        id = scrapertools.find_single_match(bloque, '([^"]+)"')
        url = scrapertools.find_single_match(bloque, '<a href="([^"]+)"')
        part = scrapertools.find_single_match(bloque, 'title="([^<]+)</a>')
        name = part[27:len(part)]
        itemlist.append( Item(channel=item.channel, action="contenido_lista", title=name, url="http://www.rtve.es/alacarta/filterVideoSlide.shtml?ctx="+id+"&seasonFilter=-1" , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    
    data = scrapertools.find_single_match(data, 'class="siguiente">(.*?)</li>')
    next = scrapertools.find_single_match(data, '<a name="paginaIR" href="([^"]+)"').replace("&amp;", "&").replace("?pbq=","?paginaBusqueda=")
    if next != "":
        itemlist.append( Item(channel=item.channel, action="listado", title="[COLOR blue]Siguiente pagina >>[/COLOR]", url="http://www.rtve.es"+next , thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    
    return itemlist

	
def contenido_lista(item):
    itemlist = []        
    # Cargar lista de contenido
    data2 = scrapertools.cache_page(item.url)
    matches = re.compile('<li class="thumbox">(.*?)</li>', re.DOTALL).findall(data2)
    for bloque in matches:
        title = scrapertools.find_single_match(bloque,'<a title="([^"]+)"')
        img = scrapertools.find_single_match(bloque,'src="([^"]+)"')
        url = "http://www.rtve.es"+scrapertools.find_single_match(bloque,'<a href="([^"]+)"')
        itemlist.append( Item(channel=item.channel, action="episodio", title=title, url=url , thumbnail=img , plot="" , viewmode="movie_with_plot", folder=True) )
    
    return itemlist
