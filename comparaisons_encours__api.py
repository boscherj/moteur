# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from mot_get_links import *
from datetime import date, datetime, timedelta
import mysql.connector
from touslessites import *
from requests_oauthlib import OAuth1

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


headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
wcapi = initBDD()
wcapi2 = initBDDremote()

site_local = 1
site_remote = 2
site_local_et_remote = 3


# Pour rappel : produit_actif est une variable gloable déclarée dans enregistrement
# produit_actif est mis à jour à chaque lecture de produit


# ------------------------------------------------------------------------------------------------------------
# RECHERCHE DE TOUTES LES CATEGORIES
# ------------------------------------------------------------------------------------------------------------
def init_woocommerce_categories():
	#l'objet retourné est un dictionnaire
	toutes_les_categories = k=wcapi.get("products/categories").json()
	l = k["product_categories"]
	return(l)

# ------------------------------------------------------------------------------------------------------------
# RECHERCHE DU SLUG DE LA CATEGORIE A PARTIR DE SON NOM
# ------------------------------------------------------------------------------------------------------------	
def search_woocommerce_category_slug(l, nom):
	for cat in l:
			if cat["name"] == nom:
				return cat["slug"]
		
	
# ------------------------------------------------------------------------------------------------------------
# COMPARAISON DU PRIX EN BDD ET DU NOM LU SUR LE SITE
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
	s1 = titre_produit_en_bdd.replace("  ", " ")
	s1 = " ".join(s1.split())
	# http://stackoverflow.com/questions/8270092/python-remove-all-whitespace-in-a-string
	
	s2 = produit_actif.nom_produit.replace("\t", "")
	s2 = s2.replace("\r", "")
	s2 = s2.replace("\n", "")	
	#s2 = s2.replace("  ", " ")
	s2 = " ".join(s2.split())
	
	#print "titre_produit_en_bdd. : "
	#print s1
	#print "produit_actif"
	#print s2
	return(s1 in s2)	


# ------------------------------------------------------------------------------------------------------------
# DESTRUCTION D'UN ENREGISTREMENT
# ------------------------------------------------------------------------------------------------------------	
def destruction_enregistrement_bdd(numero_enregistrement, all):
# Concernant le parametre all
# site_local = 1
# site_remote = 2
# site_local_et_remote = 3


	x1="products/"
	y1=str(numero_enregistrement)
	z1=x1+y1
	
	z2 = z1+"?force=true"
	
	# Destruction en local
	if (all==site_local or all==site_local_et_remote):
		try:
			print "Destruction en local de ", z2
			print(wcapi.delete(z2).json())
		except:
			return
	
	#Destruction sur les-bougies.com
	if (all==site_remote or all==site_local_et_remote):
		try:
			print "Destruction en remote de ", z2
			print(wcapi2.delete(z2).json())
		except:
			return
	
	return
	

# ------------------------------------------------------------------------------------------------------------
# MEMORISATION DES MODIFICATIONS
# ------------------------------------------------------------------------------------------------------------	
def cnx_mysql():
	print "cnx_mysql"
	cnx = mysql.connector.connect(user='jboscher', password='JBSJBSjbs1', host='localhost', port='8889', database='bougies')
	return cnx




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
liste_des_categories = init_woocommerce_categories()

# ------------------------------------------------------------------------------------------------------------
# LECTURE DU FICHIER DES ENREGISTREMENTS 
# ------------------------------------------------------------------------------------------------------------	
# SELECT ID FROM `wp_posts` WHERE `post_type` LIKE 'product' INTO OUTFILE 'filename' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
# /Applications/MAMP/db/mysql/bougies
#
# Pour n'avoir que la Lumiere des Fees
# SELECT ID FROM `wp_posts` WHERE `post_content` REGEXP 'lumiere' AND `post_type` LIKE 'product'INTO OUTFILE 'lumiere.txt' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
# FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'


lines = tuple(open("filename.txt", 'r'))

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
	# En local
	if (local_ou_remote == site_local):
		try:
			produit_dans_la_bdd=wcapi.get(z1).json()
		except:
			print "Erreur de lecture de la BDD en local"
			return
	
	#Lecture en remote
	if (local_ou_remote == site_remote):
		try:
			produit_dans_la_bdd=wcapi2.get(z1).json()
		except:
			print "Erreur de lecture de la BDD en local"
			return
			
			
	#Description du produit (en BDD)	
	try:
		description_produit_dans_la_bdd=produit_dans_la_bdd["product"]["description"]
		#print "Description : "
		#print description_produit_dans_la_bdd
	except:
		print "Erreur de lecture"
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
	categorie_produit_en_bdd = produit_dans_la_bdd["product"]["categories"][0]
	slug_categorie_produit_en_bdd = search_woocommerce_category_slug(liste_des_categories, categorie_produit_en_bdd)
	#print "categorie_produit_en_bdd", categorie_produit_en_bdd


	#On récupère le titre
	titre_produit_en_bdd = produit_dans_la_bdd["product"]["title"]
	#print "titre_produit_en_bdd", titre_produit_en_bdd

	#On récupère le prix
	prix_produit_en_bdd = produit_dans_la_bdd["product"]["price"]
	#print "prix_produit_en_bdd", prix_produit_en_bdd


	#On récupère le prix soldé
	prix_solde_produit_en_bdd = produit_dans_la_bdd["product"]["sale_price"]
	#print "prix_solde_produit_en_bdd", prix_solde_produit_en_bdd


	# Puis on lit sur Internet le fichier correpondant à l'URL
	try:
		html = requests.get(url_produit_dans_la_bdd, headers=headers) 
	except:
		print "Erreur de lecture de la page"
		#Ajout JBS le 3/6/2016
		destruction_enregistrement_bdd(numero_du_produit, local_ou_remote)
		return

	#data = html.content
	#bsObj = BeautifulSoup(data)
	
	
	site_etudie = Site()
	#print "slug : ", slug_categorie_produit_en_bdd
	site_etudie.creation(slug_categorie_produit_en_bdd)
	
	bsObj = retourne_bsObj(site_etudie, url_produit_dans_la_bdd, headers)
	
	for x in bsObj.findAll('script'):
		bsObj.script.extract()
	for x in bsObj.findAll('noscript'):
		bsObj.noscript.extract()
	

	
	get_GenericProduct(bsObj, site_etudie, url_produit_dans_la_bdd)

	print "Produit : " 
	print numero_du_produit
	if comparaison_du_nom(titre_produit_en_bdd) :
		compareprix = comparaison_du_prix(prix_produit_en_bdd) 
		if compareprix == True:
			print "Produit identique", titre_produit_en_bdd
		
		else:
			print "Prix différent : "
			print "Prix en BDD : "
			print prix_produit_en_bdd
			print "Prix lu sur le site : "
			print produit_actif.nom_produit
			
			produit_actif.add_UrlProduit(url_produit_dans_la_bdd)
			categorie=site_etudie.categorie
			produit_actif.add_Categorie_Produit(categorie)
			
			if compareprix != -2 :
				#storeProduitActif(wcapi, categorie)
				#mise à jout du produit
				#creation du produit au format Woocommerce
				data_product = create_data_4woocommerce()
				print "z1", z1
				print "data_product", data_product
				
				if data_product != None:
					#maj du produit en BDD
					#JBS le 28/9/2016
					#On détruit et on ajoute
					
					# On detruit l'enregistrement
					destruction_enregistrement_bdd(numero_du_produit, local_ou_remote)
					#memorisation_modifications(cnx, produit_dans_la_bdd, 5)
				
					# Puis on l'ajoute
					try:
						#JBS le 28/9/2016
						#print(wcapi.put(z1, data_product).json())
						storeProduitActif(wcapi, categorie)
						print "Ajout du produit local dans la liste"
					except:
						return
					
					#maj du produit sur les-bougies.com 
					try:
						#JBS le 28/9/2016
						#print(wcapi2.put(z1, data_product).json())
						storeProduitActif(wcapi2, categorie)
						print "Ajout du produit distant dans la liste"
					except:
						return
					
					
					#memorisation_modifications(cnx, produit_dans_la_bdd, 2)
			
			# compareprix = -2 ce qui veut dire impossibilite de comparer les prix
			# dans ce cas on supprime les enregistrements
			
			else:
				print "Pb sur les prix : "
				print titre_produit_en_bdd
				print produit_actif.nom_produit
				destruction_enregistrement_bdd(numero_du_produit, local_ou_remote)
				#memorisation_modifications(cnx, produit_dans_la_bdd, 5)

				
				
			produit_actif.reinit()

	
	else:
		print "Titre different : "
		print titre_produit_en_bdd
		print produit_actif.nom_produit
		
		destruction_enregistrement_bdd(numero_du_produit, local_ou_remote)
		
		#memorisation_modifications(cnx, produit_dans_la_bdd, 3)
		
		print "DELETE Titre different :  "
	


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
			oauth_consumer_key = 'cL97sM96ICTc'
			oauth_consumer_secret = 'PowjBi8BJjNQKJA0L7qKtAyfY0tC1VyPTR6H4zjfTYLLISnw'
			oauth_token = 'WuLq1eekRj6C26tQKs6z9MhG'
			oauth_token_secret = 'dqgskeOfbA5iQwiN30xjBdrhzL61PzkTtnIjlx2YsNUgDRDg'

			url = 'http://localhost:8888/bougies-parfumes-oqb.fr/wp-json/myapiplugin/v2/greeting/'

		else:
			#remote
			oauth_consumer_key = '47yuehfsAgpj'
			oauth_consumer_secret = 'ycqL7mKr6dL1ivE3Zk8yhZVNQ1oWYMaOIT74LscBU7TENXWw'
			oauth_token = 'Q1ZFhXw644lgqcSAnHN1g5Wu'
			oauth_token_secret = 'gOZalVUsuIl0GTFSUfSPU4uXfEoxBPE0mddQ4psjnAwXR54T'
			url = 'http://www.les-bougies.com/wp-json/myapiplugin/v2/greeting/'
			

	except:
		print "Echec de Init de la BDD "
		return False
	
	#Le parametre 1 indique qu'on veut la liste des numeros des produits de la categorie : categorie_du_produit
	url=url+"1/"+categorie_du_produit
	
	auth = OAuth1(oauth_consumer_key, oauth_consumer_secret,oauth_token, oauth_token_secret)
	response = requests.get(url, auth=auth)
	#response_txt = response.text
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
		#id_produits = comparaison_produits(nom_de_la_marque, site_local)
		#print id_produits
		#parcours_liste(id_produits, site_local)
		
	except:
		print "Echec de suppression_produits_categorie local"
	
	try:
		print "en remote : "
		id_produits = comparaison_produits(nom_de_la_marque, site_remote)
		print id_produits
		parcours_liste(id_produits, site_remote)
		
	except:
		print "Echec de suppression_produits_categorie remote"
	
	#print id_produits	
	
# ------------------------------------------------------------------------------------------------------------

i=0
longueur_cat = len(liste_categories_0)
print "Longueur de la liste", longueur_cat

while i < longueur_cat:
	comparaison_produits_categorie(liste_categories_0[i])
	#liste_produits.store_ProduitListe(wcapi)
	liste_produits.store_ProduitListe(wcapi2)
	liste_produits.vide_ProduitListe()
	i = i +1

