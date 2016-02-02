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

url_etudiee = "http://lalumieredesfees.fr/"

#on cherche le CMS du domain
cms, categorie = check_cms(url_etudiee)

#on parcourt tous les liens
url_format = "\/bougie"


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
# http://www.comptoir-de-famille.com/fr/senteurs/notre-offre/bougies.html
# www.comptoir-de-famille.com\/fr\/senteurs\/notre-offre\/bougies
# http://www.synopsisparis.com/
# synopsisparis.com\/fr
# http://www.decosdumonde.com/bougies-parfumees.html
# www.decosdumonde.com\/bougie
# http://www.lebonmarche.com/catalogue/maison/bougies-et-parfums-d-interieur.html
# www.lebonmarche.com\/produit\/15
# http://www.sia-homefashion.fr/produits/bougies/bougies-parfumees.html
# www.sia-homefashion.fr\/produits\/bougies
# http://www.laboiteabougies.fr/
# www.laboiteabougies.fr
# http://lalumieredesfees.fr/
# \/bougie

# http://www.scandles.fr/
# scandles.fr