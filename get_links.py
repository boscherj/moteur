import requests
import re
from bs4 import BeautifulSoup
from urlparse import urlparse
from check_cms import *
from url_accepted import *
from get_product_data import *
from enregistrement import *
 

#la liste des pages		
pages = set()


def getLinksInit(pageUrl, cms, pageUrlFormat, categorie):
	global global_regexes
	global global_cms
		
	global_regexes = re.compile(pageUrlFormat)
	global_cms = cms
	
	
	wcapi = initBDD()	
	#init_Global()
	getLinks(pageUrl, wcapi, categorie)


#------------------------------------------------------------------------------

#fonction qui prend en parametre une url et son type de CMS et ajoute les liens de la page a pages
def getLinks(pageUrl, wcapi, categorie):
	global pages
	
	print pageUrl	
			
	html = requests.get(pageUrl) 
	data = html.text
	#cette page est transformee en objet bs4
	bsObj = BeautifulSoup(data)	
	
	getproductData(bsObj, global_cms)
	
	produit_actif.add_UrlProduit(pageUrl)
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
				
				#on verifie que les mots interdits ne sont pas presents dans l url
				if url_accepted(newPage): 
					getLinks(newPage, wcapi, categorie)

