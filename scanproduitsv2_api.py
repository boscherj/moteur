# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from mot_get_links import *
from datetime import date, datetime, timedelta
import mysql.connector
from touslessites import *
#from requests_oauthlib import OAuth1
from oauth_les_bougies import *
#from lot1 import *


# ------------------------------------------------------------------------------------------------------------
# CHERCHE TOUS LES PRODUITS D'UNE MARQUE, LES DETRUIT - ET RESCANNE LA MARQUE
# ------------------------------------------------------------------------------------------------------------


		
# ------------------------------------------------------------------------------------------------------------
#TRAITEMENT DES PRODUITS D'UNE CATEGORIE
def suppression_produits_categorie(nom_de_la_marque, numero_serveur):

	#Recherche de l'identifant de la categorie
	site=nom_de_la_marque
	site_etudie = Site()
	site_etudie.creation(site)
	categorie_du_produit = site_etudie.categorie

	try:
		if numero_serveur==1:
			#local
			#oauth_consumer_key = 'cL97sM96ICTc'
			#oauth_consumer_secret = 'PowjBi8BJjNQKJA0L7qKtAyfY0tC1VyPTR6H4zjfTYLLISnw'
			#oauth_token = 'WuLq1eekRj6C26tQKs6z9MhG'
			#oauth_token_secret = 'dqgskeOfbA5iQwiN30xjBdrhzL61PzkTtnIjlx2YsNUgDRDg'

			url = 'http://localhost:8888/bougies-parfumes-oqb.fr/wp-json/myapiplugin/v2/greeting/'

		else:
			#remote
			#oauth_consumer_key = '47yuehfsAgpj'
			#oauth_consumer_secret = 'ycqL7mKr6dL1ivE3Zk8yhZVNQ1oWYMaOIT74LscBU7TENXWw'
			#oauth_token = 'DgHswn4Sr7RzGBtmtWVgqCJZ'
			#oauth_token_secret = 'zDtKFy60uyb2TA5j4B5VkWMTDEvC4TO4XlBoCCtnofY9qRfK'
			url = 'http://www.les-bougies.com/wp-json/myapiplugin/v2/greeting/'
			

	except:
		print "Echec de Init de la BDD "
		return False
	
	url=url+"100769/"+categorie_du_produit
	
	#auth = OAuth1(oauth_consumer_key, oauth_consumer_secret,oauth_token, oauth_token_secret)
	auth1 = getOauth1(numero_serveur)
	
	response = requests.get(url, auth=auth1)
	print(response.text)
	return response


# ------------------------------------------------------------------------------------------------------------
#SUPPRESSION ET AJOUT
def suppression_et_ajout_produits_categorie(nom_de_la_marque):
	print "Traitement de ", nom_de_la_marque

	try:
		print "en local : "
		#suppression_produits_categorie(nom_de_la_marque, 1)
	except:
		print "Echec de suppression_produits_categorie local"
	
	try:
		print "en remote : "
		suppression_produits_categorie(nom_de_la_marque, 2)
	except:
		print "Echec de suppression_produits_categorie remote"
		
		
	print "getLinksInit", nom_de_la_marque
	getLinksInit(nom_de_la_marque)


i=0
longueur_cat = len(liste_categories_0)
print "Longueur de la liste", longueur_cat

while i < longueur_cat:
	suppression_et_ajout_produits_categorie(liste_categories_0[i])
	i = i +1
		
