# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para busquedas Youtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import sys
import urlparse
import os

from core import config
from core import logger
from core import scrapertools
from core import jsontools
from core.item import Item
from channels import youtube_channel

key = youtube_channel.YOUTUBE_V3_API_KEY

__ordbusq__ = int(config.get_setting('ordenbusqueda', 'youtube_search'))
__tipbusq__ = int(config.get_setting('tipobusqueda', 'youtube_search'))


# Crear lista inicial del canal
def main_list(canal):
    logger.info("pelisalacarta.channels.youtube_search main_list")
    itemlist = []
    
    # Obtener datos del canal
    channel_xml = os.path.join(config.get_runtime_path(), 'channels', canal+".xml")
    infile = open(channel_xml, "rb")
    fdata = infile.read()
    infile.close()
    data = scrapertools.find_single_match(fdata, "<data>(.*?)</data>")
    
    # Mostrar lista de generos
    matches = scrapertools.find_multiple_matches(data, "<name>([^<]*)</name>")
    for titulo in matches:
        itemlist.append( Item(channel="youtube_search", server="youtube_search", action="genero", title="[B]"+titulo+"[/B]" , url=titulo, thumbnail="" , plot=canal , viewmode="movie_with_plot", folder=True) )
    
    itemlist.append( Item(channel="youtube_search", server="youtube_search", action="configura", title="[COLOR yellow][B]Configuración[/B][/COLOR]" , url=titulo, thumbnail="" , plot=canal , viewmode="movie_with_plot", folder=True) )
    return itemlist


# Procesar las entradas de cada genero
def genero(item):
    itemlist = []
    
    channel_xml = os.path.join(config.get_runtime_path(), 'channels', item.plot+".xml")
    infile = open(channel_xml, "rb")
    fdata = infile.read()
    infile.close()
    data = scrapertools.find_single_match(fdata, "<name>"+item.url+"</name>(.*?)</genero>")
    
    itemlist.append( Item(channel=item.channel, action="", title="[COLOR yellow][B]"+item.url.upper()+"[/B][/COLOR]" , url="", thumbnail="" , plot="" , viewmode="movie_with_plot", folder=True) )
    matches = scrapertools.find_multiple_matches(data, "<item>(.*?)</item>")
    for match in matches:
        titulo = scrapertools.find_single_match(match, "<entry>([^<]*)</entry>")
        search = scrapertools.find_single_match(match, "<search>([^<]*)</search>")
        full_list = scrapertools.find_single_match(match, "<full_list>([^<]*)</full_list>")
        if search != "":
            itemlist.append( Item(channel=item.channel, action="filtra", title=titulo , url=make_url_search(search), thumbnail="" , plot=item.title , viewmode="movie_with_plot", folder=True) )
        if full_list != "":
            itemlist.append( Item(channel=item.channel, action="full_list", title=titulo , url=full_list, thumbnail="" , plot=item.title , viewmode="movie_with_plot", folder=True) )
    
    return itemlist


# Seleccionar modo del filtro
def filtra(item):
    if __tipbusq__ == 0:
        return filtra_video(item)
    if __tipbusq__ == 1:
        return filtra_lista(item)


# Muestra el resultado de busqueda listas
def filtra_lista(item):
    itemlist = []
    data = scrapertools.cache_page(item.url)
    json_object = jsontools.load_json(data)
    for row in json_object['items']:
        itemlist.append( Item(channel=item.channel, action="lista_channelid", title=row['snippet']['title'] + " ([COLOR yellow]Lista[/COLOR])", url=make_list_page(row['id']['playlistId']) , thumbnail=row['snippet']['thumbnails']['high']['url'] , plot=row['snippet']['title'].upper() , viewmode="movie_with_plot", folder=True) )
    # Quitar token previo si existe
    if item.url.find("&nextPageToken")>0:
        item.url=item.url[:item.url.len()-21]
    # Siguiente pagina de busqueda
    try:
        next = item.url + "&pageToken="+json_object['nextPageToken']
        itemlist.append( Item(channel=item.channel, action="filtra_lista", title=">> Pagina siguiente" , url=next, plot=item.title, folder=True, viewmode="movie_with_plot") )
    except:
        logger.info('Ultima pagina')
    return itemlist


# Muestra el resultado de busqueda videos
def filtra_video(item):
    itemlist = []
    data = scrapertools.cache_page(item.url)
    json_object = jsontools.load_json(data)
    for row in json_object['items']:
        itemlist.append( Item(channel=item.channel, action="play", server="youtube", title=row['snippet']['title'] , url="https://www.youtube.com/watch?v="+row['id']['videoId'] , thumbnail=row['snippet']['thumbnails']['high']['url'] , plot="" , viewmode="movie_with_plot", folder=True) )
    # Quitar token previo si existe
    if item.url.find("&nextPageToken")>0:
        item.url=item.url[:item.url.len()-21]
    # Siguiente pagina de busqueda
    try:
        next = item.url + "&pageToken="+json_object['nextPageToken']
        itemlist.append( Item(channel=item.channel, action="filtra", title="[COLOR blue]>> Pagina siguiente[/COLOR]" , url=next , folder=True, viewmode="movie_with_plot") )
    except:
        logger.info('Ultima pagina')
    return itemlist


# Listar contenido del canal
def lista_channelid(item):
    itemlist = []
    data = scrapertools.cache_page(item.url)
    json_object = jsontools.load_json(data)
    itemlist.append( Item(channel=item.channel, action="", title="[COLOR red]"+item.plot+"[/COLOR]", url="", folder=True, viewmode="movie_with_plot") )
    for row in json_object['items']:
        titulo = row['snippet']['title']
        if titulo != "Deleted video":
            itemlist.append( Item(channel=item.channel, action="play", server="youtube", title=titulo , url="https://www.youtube.com/watch?v="+row['snippet']['resourceId']['videoId'] , thumbnail=row['snippet']['thumbnails']['high']['url'] , plot="" , viewmode="movie_with_plot", folder=True) )
    
    # Quitar token previo si existe
    if item.url.find("&nextPageToken")>0:
        item.url=item.url[:item.url.len()-21]
    # Siguiente pagina si existe
    try:
        next = item.url + "&pageToken="+json_object['nextPageToken']
        itemlist.append( Item(channel=item.channel, action="lista_channelid", title="[COLOR blue]>> Pagina siguiente[/COLOR]" , url=next , folder=True, viewmode="movie_with_plot") )
    except:
        logger.info('Ultima pagina')
    return itemlist


# Crear cadena de busqueda
def make_url_search(texto):
    # Ajustar orden
    ord = ""
    if __ordbusq__ == 0:
        ord = "&order=relevance"
    if __ordbusq__ == 1:
        ord = "&order=date"
    # Ajustar tipo
    typ = "&type=video"
    if __tipbusq__ == 1:
        typ = "&type=playlist"
    
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + texto + "&key=" + key + "&maxResults=50"+typ+ord
    return url


# Pagina de lista
def make_list_page(list):
    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&key="+key+"&playlistId="+list
    return url


# Menu de configuracion
def configura(item):
    from platformcode import platformtools
    platformtools.show_channel_settings()
    if config.is_xbmc():
        import xbmc
        xbmc.executebuiltin("Container.Refresh")


__max = 10

# Generar lista completa de un canal
def full_list(item):
    itemlist = []
    mas = 1
    next = item.url
    url = item.url.split("&pageToken=")[0]
    
    while (mas<__max):
        data = scrapertools.cache_page(make_list_page(next))
        json_object = jsontools.load_json(data)
        # Solo para el comienzo poner titulo
        if mas==1:
            itemlist.append( Item(channel=item.channel, action="", title="[COLOR red]"+item.plot+"[/COLOR] "+"("+str(json_object['pageInfo']['totalResults'])+")", url="", folder=True, viewmode="movie_with_plot") )
        for row in json_object['items']:
            titulo = row['snippet']['title']
            if titulo != "Deleted video":
                itemlist.append( Item(channel=item.channel, action="play", server="youtube", title=titulo.capitalize() , url="https://www.youtube.com/watch?v="+row['snippet']['resourceId']['videoId'] , thumbnail=row['snippet']['thumbnails']['high']['url'] , plot="" , viewmode="movie_with_plot", folder=True) )
        mas = mas + 1
        try:
            next = url + "&pageToken="+json_object['nextPageToken']
        except:
            mas = 1000
    
    # Si aun quedan mas entradas
    if mas==__max:
        itemlist.append( Item(channel=item.channel, action="full_list", title="[COLOR blue]Siguiente >>[/COLOR]" , url=next , thumbnail="" , plot=item.plot , viewmode="movie_with_plot", folder=True) )
    
    return itemlist


