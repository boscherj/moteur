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

url_etudiee = "http://www.lebonmarche.com/catalogue/maison/bougies-et-parfums-d-interieur.html"

#on cherche le CMS du domain
cms, categorie = check_cms(url_etudiee)

#on parcourt tous les liens
url_format = "www.lebonmarche.com\/produit\/15"

getLinksInit(url_etudiee, cms, url_format, categorie)


