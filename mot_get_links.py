# -*- coding: utf-8 -*-

import requests
import re
import dryscrape
from bs4 import BeautifulSoup
from urlparse import urlparse
from check_cms import *
from url_accepted import *
from mot_get_product_data_generic_parameter import *
from enregistrement import *
#from tools_moteur import *
from mot_generic_tools import * 

#la liste des pages		
pages = set()


def getLinksInit(site):
	global global_regexes
	global global_cms
	global global_netloc
	global global_scheme
	
	print "getLinksInit"
	site_etudie = Site()
	site_etudie.creation(site)
	global_cms = cms = site_etudie.cms
	pageUrl = site_etudie.url_etudiee
	pageUrlFormat = site_etudie.url_format
	categorie = site_etudie.categorie
		
	global_regexes = re.compile(pageUrlFormat)
	
	
	wcapi = initBDD()	
	#init_Global()
	
	parsed_url = urlparse(pageUrl)
	global_netloc = parsed_url.netloc
	global_scheme = parsed_url.scheme
	
	getLinks(pageUrl, wcapi, site_etudie)
	
	#liste_produits.print_ProduitListe()
	liste_produits.store_ProduitListe(wcapi)

#------------------------------------------------------------------------------

#fonction qui prend en parametre une url et son type de CMS et ajoute les liens de la page a pages
def getLinks(pageUrl, wcapi, site_etudie):
	global pages
	
	print "..."
	print pageUrl	
	
	#Pour l'Occitane (accents dans les url)
	#pageUrl = rem_accents(pageUrl)
	#
	
	#if doit_on_utiliser_dryscrape(site_etudie):
		#session = dryscrape.Session()
		#session.visit(pageUrl)
		#response = session.body()
		#bsObj = BeautifulSoup(response)
	#else:	
	html = requests.get(pageUrl) 
	
	# http://stackoverflow.com/questions/25483726/python-encoding-error-not-unicode-string
	# auparavant je faisais data = html.text
	# ce qui entrainait des problèmes avec les accents
	data = html.content
	#cette page est transformee en objet bs4
	bsObj = BeautifulSoup(data)	
	
	#getproductData(bsObj, global_cms)
	get_GenericProduct(bsObj, site_etudie, pageUrl)
	
	
	produit_actif.add_UrlProduit(pageUrl)
	
	categorie=site_etudie.categorie
	produit_actif.add_Categorie_Produit(categorie)
	#produit_actif.printProduit()
	storeProduitActif(wcapi, categorie)
	
	produit_actif.reinit()
                                     
	for link in bsObj.findAll("a", href=global_regexes):
		#si c'est un lien
		if 'href' in link.attrs:
			#si le lien n'a pas ete traite
			if link.attrs['href'] not in pages:
			#We have encountered a new page
				
				newPage = link.attrs['href'] 
				pages.add(newPage) 
				#print newPage
				
				#Pour la lumiere des fees car les URL ne sont pas completes
				parsed_url = urlparse(newPage)
				if parsed_url.netloc == "":
					newPage = global_scheme + "://" + global_netloc + newPage	
					#print newPage
				
				#on verifie que les mots interdits ne sont pas presents dans l url
				if url_accepted(newPage): 
					getLinks(newPage, wcapi, site_etudie)

