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

from enregistrement import *
from xml.sax.saxutils import escape
from mot_generic_tools import *
import dryscrape
from mot_generic_tools import * 
from urlparse import urlparse
from mot_get_product_data_generic_parameter import *
from url_accepted import *

# JBS Ajout le 6/7/2016
from datetime import date, datetime, timedelta
import mysql.connector

# JBS Ajout le 4/5/2017
import xml.sax.saxutils as saxutils

from oauth_les_bougies import *


headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
#wcapi = initBDD()
wcapi = initBDD_2()
#wcapi2 = initBDDremote()
wcapi2 = initBDDremote_2()

site_local = 1
site_remote = 2
site_local_et_remote = 3

const_destruction_produit = 1
const_maj_produit = 2


CRED = '\033[91m'
CEND = '\033[0m'


# Pour rappel : produit_actif est une variable gloable déclarée dans enregistrement
# produit_actif est mis à jour à chaque lecture de produit
# produit_actif est déclaré en global dans enregistrement

# ------------------------------------------------------------------------------------------------------------
# RECHERCHE DE TOUTES LES CATEGORIES
# ------------------------------------------------------------------------------------------------------------
def init_woocommerce_categories():
	#l'objet retourné est un dictionnaire
	toutes_les_categories = k=wcapi.get("products/categories").json()
	l = k["product_categories"]
	return(l)

# RECHERCHE DE TOUTES LES CATEGORIES V2 
# ------------------------------------------------------------------------------------------------------------
def init_woocommerce_categories_v2():
	#l'objet retourné est une liste
	# On a moins de 200 catégories
	toutes_les_categories=wcapi.get("products/categories?per_page=100&page=1").json()
	k2=wcapi.get("products/categories?per_page=100&page=2").json()
	
	toutes_les_categories.extend(k2)
	# l = k["product_categories"]
	return(toutes_les_categories)


# ------------------------------------------------------------------------------------------------------------
# RECHERCHE DU SLUG DE LA CATEGORIE A PARTIR DE SON NOM
# ------------------------------------------------------------------------------------------------------------	
def search_woocommerce_category_slug(l, id):
	for cat in l:
			if cat["id"] == id:
				return cat["slug"]
		
	
# ------------------------------------------------------------------------------------------------------------
# COMPARAISON DU PRIX EN BDD ET DU NOM LU SUR LE SITE
# La valeur -2 est retournée si la comparaison est impossible
# La valeur 1 est retournée si les prix sont identiques
# Sinon la valeur retournée est 0
# ------------------------------------------------------------------------------------------------------------	
def comparaison_du_prix(prix_produit_en_bdd):
	#print "prix_produit_en_bdd", prix_produit_en_bdd
	try:
		x = float(prix_produit_en_bdd)
	except:	
		return (-2)	
	
	try:
		y = float(produit_actif.prix_produit)
	except:	
		return (-2)	
		
	return(x==y)
		
# ------------------------------------------------------------------------------------------------------------
# COMPARAISON DU NOM EN BDD ET DU NOM LU SUR LE SITE
# ------------------------------------------------------------------------------------------------------------	
def comparaison_du_nom(titre_produit_en_bdd):

	#print "titre_produit_en_bdd avant modif : ", titre_produit_en_bdd
	#print "titre_produit en remote avant modif : ", produit_actif.nom_produit
	
	s1 = saxutils.unescape(titre_produit_en_bdd) 	
	s1 = s1.replace("\t", "")
	s1 = s1.replace("\r", "")
	s1 = s1.replace("\n", "")	
	
	s1 = s1.replace("  ", " ")
	s1 = " ".join(s1.split())
	# http://stackoverflow.com/questions/8270092/python-remove-all-whitespace-in-a-string
	
	s2 = saxutils.unescape(produit_actif.nom_produit) 
	s2 = s2.replace("\t", "")
	s2 = s2.replace("\r", "")
	s2 = s2.replace("\n", "")	
	#s2 = s2.replace("  ", " ")
	s2 = " ".join(s2.split())
	
	print "comparaison_du_nom : "
	print "titre_produit_en_bdd. : "
	print s1
	print "produit_actif"
	print s2
	print "--------------------"
	
	return(s1 in s2)	


# ------------------------------------------------------------------------------------------------------------
# DESTRUCTION D'UN ENREGISTREMENT
# ------------------------------------------------------------------------------------------------------------	
def destruction_enregistrement_bdd(numero_enregistrement, all, produit_dans_la_bdd):
# Concernant le parametre all
# site_local = 1
# site_remote = 2
# site_local_et_remote = 3

	# memorisation_modifications_2(produit_en_bdd, numero_serveur, numero_du_produit, del_ou_updt)
	
	#memorisation_modifications_2(produit_dans_la_bdd, all, numero_enregistrement, const_destruction_produit)
	
	x1="products/"
	y1=str(numero_enregistrement)
	z1=x1+y1
	
	z2 = z1+"?force=true"
	
	# Destruction en local
	if (all==site_local or all==site_local_et_remote):
		try:
			#print "Destruction en local de ", z2
			print(CRED + "Destruction en local de " + CEND), z2
			print(wcapi.delete(z2).json())
		except:
			return
	
	#Destruction sur les-bougies.com
	if (all==site_remote or all==site_local_et_remote):
		try:
			#print "Destruction en remote de ", z2
			print(CRED + "Destruction en local de " + CEND), z2
			print(wcapi2.delete(z2).json())
		except:
			return
	
	return
	

# ------------------------------------------------------------------------------------------------------------
# CONNEXION A LA BDD - OBSOLETE
# ------------------------------------------------------------------------------------------------------------	
def cnx_mysql():
	print "cnx_mysql"
	cnx = mysql.connector.connect(user='jboscher', password='xxxxxxxxx', host='localhost', port='8889', database='bougies')
	return cnx

# ------------------------------------------------------------------------------------------------------------
# MEMORISATION DES MODIFICATIONS
# ------------------------------------------------------------------------------------------------------------	
def memorisation_modifications_2(produit_en_bdd, numero_serveur, numero_du_produit, del_ou_updt):
	#print "produit_en_bdd : ", produit_en_bdd
	#print "numero_serveur : ", numero_serveur
	# del_ou_updt : const_destruction_produit, const_maj_produit
	
	print "Numero :", numero_du_produit
		
	if produit_actif.prix_produit != None:
		print produit_actif.prix_produit
		
	if produit_actif.prix_ancien_produit != None:
		print produit_actif.prix_ancien_produit
		
	if produit_actif.prix_special_produit != None:
		print produit_actif.prix_special_produit

		
		
	#Recuperation de la liste des numeros des produits
	#Le parametre 1 indique qu'on veut la liste des numeros des produits de la categorie : categorie_du_produit
	# Appel de l'API REST memorisation
	
	# memorisation/(?P<ID_post_modifie>\d+)&(?P<del_ou_updt>\d+)&(?P<ancien_prix_affiche>\d+)&(?P<ancien_prix_solde>\d+)
	if numero_serveur==site_local:
		#local
		url = 'http://localhost:8888/bougies-parfumes-oqb.fr/'

	else:
		#remote
		url = 'http://www.les-bougies.com/'
		
	# Ajout de ID_post_modifie
	url = url + 'wp-json/myapiplugin/v2/memorisation/'
	url=url+str(numero_du_produit)
	
	# Ajout de del_ou_updt 
	url=url+'&'+str(del_ou_updt)

	
	# Ajout de ancien_prix_affiche
	ancien_prix_affiche = prix_du_produit_v2(produit_en_bdd)
	
	# a, b = str(ancien_prix_affiche).split(".")
	url=url+'&'+str(ancien_prix_affiche)
	
	# Ajout de ancien_prix_solde 
	ancien_prix_solde = prix_solde_du_produit_v2(produit_en_bdd)
	print "ancien_prix_solde :", ancien_prix_solde
	url=url+'&'+ str(ancien_prix_solde)
			
	print "URL appelee :", url
	
	auth1 = getOauth1(numero_serveur)
	
	response = requests.get(url, auth=auth1)
	response_txt = response.text
	print response_txt
	# http://docs.python-requests.org/en/master/
	response_json = response.json()
	
	#reponse = response_json['post']
	#print reponse
	
	return response_json



# ------------------------------------------------------------------------------------------------------------
# MEMORISATION DES MODIFICATIONS
# ------------------------------------------------------------------------------------------------------------	
def memorisation_modifications(cnx, produit_en_bdd, del_ou_upd):

	print "memorisation_modifications"
	
	add_modification = ("INSERT INTO wp_modification_posts "
		"(id_post_modifie, date_modification, del_ou_updt, ancien_prix_affiche, nx_prix_affiche, ancien_prix_solde, nx_prix_solde) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s)")
	
	auj = datetime.now().date()
	
	#On récupère le prix
	prix_produit_en_bdd = produit_en_bdd["product"]["price"]
	#print "prix_produit_en_bdd", prix_produit_en_bdd
	if prix_produit_en_bdd == None:
		print "prix_produit_en_bdd = None puis 0 "
		prix_produit_en_bdd = 0

	#On récupère le prix soldé
	prix_solde_produit_en_bdd = produit_en_bdd["product"]["sale_price"]
	#print "prix_solde_produit_en_bdd", prix_solde_produit_en_bdd
	if prix_solde_produit_en_bdd == None:
		prix_solde_produit_en_bdd = 0
		print "prix_solde_produit_en_bdd = None puis 0 "
	
	#On récupère l'ID
	id_produit_en_bdd = produit_en_bdd["product"]["id"]
	
	#Prix lu sur le site distant 
	prix_produit_distant = produit_actif.prix_produit
	#print "prix_produit_distant", prix_produit_distant
	if prix_produit_distant == None:
		prix_produit_distant = 0
	
	
	#Prix solde lu sur le site distant 
	prix_solde_produit_distant = produit_actif.prix_special_produit
	#print "prix_solde_produit_distant", prix_solde_produit_distant
	if prix_solde_produit_distant == None:
		prix_solde_produit_distant = 0
	
	cursor = cnx.cursor()
	

	data_modification = (id_produit_en_bdd, auj, del_ou_upd, prix_produit_en_bdd, prix_produit_distant, prix_solde_produit_en_bdd, prix_solde_produit_distant)
	cursor.execute(add_modification, data_modification)
	
	cnx.commit()
	cursor.close()

	return



			
# ------------------------------------------------------------------------------------------------------------
# INIT DE LA LA LISTE DES CATEGORIES
# ------------------------------------------------------------------------------------------------------------	

# Init de la liste des categories
liste_des_categories = init_woocommerce_categories_v2()

# ------------------------------------------------------------------------------------------------------------
# LECTURE DU FICHIER DES ENREGISTREMENTS 
# ------------------------------------------------------------------------------------------------------------	
# SELECT ID FROM `wp_posts` WHERE `post_type` LIKE 'product' INTO OUTFILE 'filename' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
# /Applications/MAMP/db/mysql/bougies
#
# Pour n'avoir que la Lumiere des Fees
# SELECT ID FROM `wp_posts` WHERE `post_content` REGEXP 'lumiere' AND `post_type` LIKE 'product'INTO OUTFILE 'lumiere.txt' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
# FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'


# lines = tuple(open("filename.txt", 'r'))



# ------------------------------------------------------------------------------------------------------------
# DESCRIPTION DU PRODUIT V2 - API REST V2
# ------------------------------------------------------------------------------------------------------------	
# La fonction retourne None ou la description
# Cette fonction suppose l'API REST Woocommerce en version legacy

def description_du_produit_v2(produit):
		
	try:
		description_du_produit=produit["description"]
		# print "Description : "
		# print description_du_produit
	except:
		print "Erreur de lecture de la description"
		return None

	return description_du_produit


# ------------------------------------------------------------------------------------------------------------
# CATEGORIE DU PRODUIT V2 - API REST V2
# ------------------------------------------------------------------------------------------------------------	
# La fonction retourne None ou la categorie du produit
# Cette fonction suppose l'API REST Woocommerce en version legacy

def categorie_du_produit_v2(produit):
		
	try:
		categorie_produit = produit["categories"][0]['id']
		print "Categorie : "
		print categorie_produit
	except:
		print "Erreur de lecture de categorie"
		return None
		
	return categorie_produit


# ------------------------------------------------------------------------------------------------------------
# TITRE DU PRODUIT V2 - API REST V2
# ------------------------------------------------------------------------------------------------------------	
# La fonction retourne None ou le titre du produit
# Cette fonction suppose l'API REST Woocommerce en version legacy

def titre_du_produit_v2(produit):
		
	try:
		titre_du_produit = produit["name"]
		#print "Titre : "
		#print titre_du_produit
	except:
		print "Erreur de lecture du titre"
		return None

	return titre_du_produit
	
# ------------------------------------------------------------------------------------------------------------
# PRIX DU PRODUIT V2 - API REST V2
# ------------------------------------------------------------------------------------------------------------	
# La fonction retourne None ou le titre du produit
# Cette fonction suppose l'API REST Woocommerce en version legacy

def prix_du_produit_v2(produit):
		
	try:
		prix_produit = produit["price"]
		print "Prix : "
		print prix_produit
	except:
		print "Erreur de lecture du prix"
		return None

	return prix_produit

	
	
# ------------------------------------------------------------------------------------------------------------
# PRIX SOLDE DU PRODUIT V2 - API REST V2
# ------------------------------------------------------------------------------------------------------------	
# La fonction retourne None ou le titre du produit
# Cette fonction suppose l'API REST Woocommerce en version legacy

def prix_solde_du_produit_v2(produit):
	
	# print "prix_solde_du_produit_v2 ", produit
	prix_solde_produit=0
	
	try:
		prix_solde_produit = produit["sale_price"]
		print "Prix solde: "
		print prix_solde_produit
		if prix_solde_produit =="":
			prix_solde_produit=0
	except:
		print "Erreur de lecture du prix solde"
	
	return prix_solde_produit


# ------------------------------------------------------------------------------------------------------------
# COMPARAISON D'UN PRODUIT
# ------------------------------------------------------------------------------------------------------------	

def comparaison_du_produit(numero_du_produit, local_ou_remote):
# local_ou_remote 1 : local, 2 : distant

	produit_actif.reinit()
	
	# Tout d'abord on lit le produit dans la BdD
	x1="products/"
	y1=str(numero_du_produit)
	z1=x1+y1
	
	#Lecture du produit dans la BDD
	if (local_ou_remote == site_local):
		w=wcapi
	else:
		w=wcapi2

	
	try:
		produit_dans_la_bdd=w.get(z1).json()
	except:
		print "Erreur de lecture de la BDD en local"
		return
	
			
	#Description du produit (en BDD)
	#	
	description_produit_dans_la_bdd=description_du_produit_v2(produit_dans_la_bdd)
	if (description_produit_dans_la_bdd == None):
		print "Erreur de lecture de la description - C"
		return
	
	#il n'y a qu'une URL dans la description, celle du lien qui mène vers le produit	
	z=re.findall("<a href.*\"", description_produit_dans_la_bdd)
	q=z[0]

	# On récupère l'URL dans la description
	# L'URL est entre guillemets
	s=re.findall("\".*\"", q)
	t=s[0]
	# On supprime les guillemets
	url_produit_dans_la_bdd=t.replace("\"","")
	#print "URL dans la BDD : "
	#print url_produit_dans_la_bdd

	#On récupère la categorie
	categorie_produit_en_bdd = categorie_du_produit_v2(produit_dans_la_bdd)
	slug_categorie_produit_en_bdd = search_woocommerce_category_slug(liste_des_categories, categorie_produit_en_bdd)
	#print "slug_categorie_produit_en_bdd : ", slug_categorie_produit_en_bdd
	#print "categorie_produit_en_bdd", categorie_produit_en_bdd


	#On récupère le titre
	titre_produit_en_bdd = titre_du_produit_v2(produit_dans_la_bdd)
	#print "titre_produit_en_bdd", titre_produit_en_bdd

	#On récupère le prix
	prix_produit_en_bdd = prix_du_produit_v2(produit_dans_la_bdd)
	#print "prix_produit_en_bdd", prix_produit_en_bdd


	#On récupère le prix soldé
	prix_solde_produit_en_bdd = prix_solde_du_produit_v2(produit_dans_la_bdd)
	#print "prix_solde_produit_en_bdd", prix_solde_produit_en_bdd


	# Puis on lit sur Internet le fichier correpondant à l'URL
	# JE PENSE QUE CES LIGNES NE SERVENT PLUS A RIEN
	try:
		html = requests.get(url_produit_dans_la_bdd, headers=headers) 
	except:
		print "Erreur de lecture de la page - C"
		#Ajout JBS le 3/6/2016
		destruction_enregistrement_bdd(numero_du_produit, local_ou_remote, produit_dans_la_bdd)
		return

	#data = html.content
	#bsObj = BeautifulSoup(data)
	
	
	site_etudie = Site()
	#print "slug : ", slug_categorie_produit_en_bdd
	site_etudie.creation(slug_categorie_produit_en_bdd)
	#print "slug_categorie_produit_en_bdd :", slug_categorie_produit_en_bdd
	
	bsObj = retourne_bsObj(site_etudie, url_produit_dans_la_bdd, headers)
	
	for x in bsObj.findAll('script'):
		bsObj.script.extract()
	for x in bsObj.findAll('noscript'):
		bsObj.noscript.extract()
	

	# Ajout JBS le 4/5/2017
	
	url_produit_dans_la_bdd = saxutils.unescape(url_produit_dans_la_bdd)
	#print "url_produit_dans_la_bdd : ", url_produit_dans_la_bdd
	#site_etudie.url_etudiee = url_produit_dans_la_bdd
	
	# Lecture du produit sur le site distant
	# get_GenericProduct retourne 1 si OK MAIS surtout met à jour la variable globale produit_actif qui contient le produit lui en remote
	#print "get_GenericProduct avant appel URL : ", url_produit_dans_la_bdd

	get_GenericProduct(bsObj, site_etudie, url_produit_dans_la_bdd)
	# print "get_GenericProduct ", url_produit_dans_la_bdd
	print "Produit actif :", produit_actif.nom_produit

	print "Produit : " 
	print numero_du_produit
	
	if comparaison_du_nom(titre_produit_en_bdd) :
		compareprix = comparaison_du_prix(prix_produit_en_bdd) 
		if compareprix == True:
			print "Produit identique", titre_produit_en_bdd
			#memorisation_modifications_2(produit_dans_la_bdd, local_ou_remote, numero_du_produit, const_maj_produit)
		
		else:
			print "Prix différent : "
			print "Prix en BDD : "
			print prix_produit_en_bdd
			print "Prix lu sur le site : "
			print produit_actif.prix_produit
			
			produit_actif.add_UrlProduit(url_produit_dans_la_bdd)
			categorie=site_etudie.categorie
			produit_actif.add_Categorie_Produit(categorie)
			
			if compareprix != -2 :
				#storeProduitActif(wcapi, categorie)
				#mise à jout du produit
				#creation du produit au format Woocommerce
				# Cette partie est inutile car storeProduitActif fait déjà le travail
				
				print(CRED + "Mise à jour de " + CEND), numero_du_produit
				majProduitActif(w, categorie, numero_du_produit)
				#memorisation_modifications(cnx, produit_dans_la_bdd, 2)
				#memorisation_modifications_2(produit_dans_la_bdd, local_ou_remote, numero_du_produit, const_maj_produit)
			
			# compareprix = -2 ce qui veut dire impossibilite de comparer les prix
			# dans ce cas on supprime les enregistrements
			
			else:
				print "Pb sur les prix : "
				print titre_produit_en_bdd
				print produit_actif.nom_produit
				destruction_enregistrement_bdd(numero_du_produit, local_ou_remote, produit_dans_la_bdd)
				#memorisation_modifications(cnx, produit_dans_la_bdd, 5)
				#memorisation_modifications_2(produit_dans_la_bdd, local_ou_remote, numero_du_produit, const_maj_produit)

			
			produit_actif.reinit()

	
	else:
		print "Titre different : "
		print "titre_produit_en_bdd : ", titre_produit_en_bdd
		print "produit_actif.nom_produit : ", produit_actif.nom_produit
		
		destruction_enregistrement_bdd(numero_du_produit, local_ou_remote, produit_dans_la_bdd)
		
		#memorisation_modifications(cnx, produit_dans_la_bdd, 3)
		#print memorisation_modifications_2(produit_dans_la_bdd, local_ou_remote)
		#print "DELETE Titre different :  "

	print "NUMERO _du_produit : ", numero_du_produit
	#print memorisation_modifications_2(produit_dans_la_bdd, local_ou_remote, numero_du_produit)	

# ------------------------------------------------------------------------------------------------------------
# COMPARE LES PRODUITS D'UNE MARQUE EN BDD REMOTE AVEC LA VERSION DU SITE MARCHAND
# ------------------------------------------------------------------------------------------------------------


		
# ------------------------------------------------------------------------------------------------------------
#TRAITEMENT DES PRODUITS D'UNE CATEGORIE
# Pour une categorie de produits donnée, retourne la liste des enregistrements concernes

def comparaison_produits(nom_de_la_marque, numero_serveur):

	#Recherche de l'identifant de la categorie
	site=nom_de_la_marque
	site_etudie = Site()
	site_etudie.creation(site)
	categorie_du_produit = site_etudie.categorie

	#Recuperation de la liste des numeros des produits
	try:
		if numero_serveur==site_local:
			#local
			#oauth_consumer_key = 'cL97sM96ICTc'
			#oauth_consumer_secret = 'PowjBi8BJjNQKJA0L7qKtAyfY0tC1VyPTR6H4zjfTYLLISnw'
			#oauth_token = 'WuLq1eekRj6C26tQKs6z9MhG'
			#oauth_token_secret = 'dqgskeOfbA5iQwiN30xjBdrhzL61PzkTtnIjlx2YsNUgDRDg'

			url = 'http://localhost:8888/bougies-parfumes-oqb.fr/'

		else:
			#remote
			#oauth_consumer_key = '47yuehfsAgpj'
			#oauth_consumer_secret = 'ycqL7mKr6dL1ivE3Zk8yhZVNQ1oWYMaOIT74LscBU7TENXWw'
			#oauth_token = 'Q1ZFhXw644lgqcSAnHN1g5Wu'
			#oauth_token_secret = 'gOZalVUsuIl0GTFSUfSPU4uXfEoxBPE0mddQ4psjnAwXR54T'
			url = 'http://www.les-bougies.com/'
			

	except:
		print "Echec de Init de la BDD "
		return False
	
	#Le parametre 1 indique qu'on veut la liste des numeros des produits de la categorie : categorie_du_produit
	url = url + 'wp-json/myapiplugin/v2/greeting/'
	url=url+"1/"+categorie_du_produit
	
	auth1 = getOauth1(numero_serveur)
	#auth = OAuth1(oauth_consumer_key, oauth_consumer_secret,oauth_token, oauth_token_secret)
	response = requests.get(url, auth=auth1)
	response_txt = response.text
	print response_txt
	# http://docs.python-requests.org/en/master/
	response_json = response.json()
	
	numeros = response_json['post']
	#print numeros
	
	
	liste_numeros=[]
	for x in numeros:
		liste_numeros.append(int(x['ID']))

	return liste_numeros

# ------------------------------------------------------------------------------------------------------------
# PARCOURS DE LA LISTE POUR COMPARAISON
def parcours_liste(liste_produits, local_ou_remote):
# local_ou_remote 1 : local, 2 : distant

	for x in liste_produits: 
		print x
		comparaison_du_produit(x, local_ou_remote)
 

# ------------------------------------------------------------------------------------------------------------
#SUPPRESSION ET AJOUT
def comparaison_produits_categorie(nom_de_la_marque):
	print "Traitement de ", nom_de_la_marque

	try:
		print "en local : "
		# La fonction comparaison_produits retourne la liste des enregistrements de la categorie
		id_produits = comparaison_produits(nom_de_la_marque, site_local)
		print id_produits
		parcours_liste(id_produits, site_local)
		
	except:
		print "Echec de suppression_produits_categorie local"
	
	try:
		print "en remote : "
		# La fonction comparaison_produits retourne la liste des enregistrements de la categorie
		#id_produits = comparaison_produits(nom_de_la_marque, site_remote)
		#print id_produits
		#parcours_liste(id_produits, site_remote)
		
	except:
		print "Echec de suppression_produits_categorie remote"
	
	#print id_produits	
	
# ------------------------------------------------------------------------------------------------------------

i=0
longueur_cat = len(liste_categories_0)
print "Longueur de la liste", longueur_cat

# Parcours de l'ensemble des sites listés dans touslessites 
while i < longueur_cat:
	comparaison_produits_categorie(liste_categories_0[i])
	# Les produits ne sont pas enregistres en fin de parcours de liste - ils sont mis à jour le long du parcours
	#liste_produits.store_ProduitListe(wcapi)
	#liste_produits.store_ProduitListe(wcapi2)
	liste_produits.vide_ProduitListe()
	i = i +1

