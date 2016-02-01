# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from get_links import *

#la liste des pages		
pages = set()
#Le type du domaine (CMS et autres infos)
global domain_type

url_etudiee = "http://www.diptyqueparis.fr/home-fragrances/candles.html"

#on cherche le CMS du domain
cms, categorie = check_cms(url_etudiee)

#on parcourt tous les liens
url_format = "\/*diptyqueparis.fr"


getLinksInit(url_etudiee, cms, url_format, categorie)


# http://www.durance.fr/
# durance.fr
# http://www.esteban.fr
# \/*esteban.fr\/fr\/
# http://www.bougies-parfums.fr/
# bougies-parfums.fr
# http://www.laboiteabougies.fr/
# www.laboiteabougies.fr
# http://www.diptyqueparis.fr/home-fragrances/candles.html
# \/*diptyqueparis.fr
