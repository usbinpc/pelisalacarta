# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Peliculas en Youtube
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
from channels import youtube_search


# Crear lista inicial del canal
def mainlist(item):
    logger.info("pelisalacarta.channels.youtube_movie mainlist")
    itemlist = []
    
    return youtube_search.main_list("youtube_movie")
