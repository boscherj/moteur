# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
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
	print "prix_produit_en_bdd", prix_produit_en_bdd
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
	s2 = produit_actif.nom_produit.replace("\t", "")
	s2 = s2.replace("\r", "")
	s2 = s2.replace("\n", "")	
	s2 = s2.replace("  ", " ")
	#print "titre_produit_en_bdd. : "
	#print s1
	#print "produit_actif"
	#print s2
	return(s1 in s2)	


# ------------------------------------------------------------------------------------------------------------
# DESTRUCTION D'UN ENREGISTREMENT
# ------------------------------------------------------------------------------------------------------------	
def destruction_enregistrement_bdd(numero_enregistrement, all):

	x1="products/"
	y1=str(numero_enregistrement)
	z1=x1+y1
	
	z2 = z1+"?force=true"
	try:
		print(wcapi.delete(z2).json())
	except:
		return
	
	#Destruction sur les-bougies.com
	if all==1:
		try:
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
	print "prix_produit_en_bdd", prix_produit_en_bdd
	if prix_produit_en_bdd == None:
		print "prix_produit_en_bdd = None puis 0 "
		prix_produit_en_bdd = 0

	#On récupère le prix soldé
	prix_solde_produit_en_bdd = produit_en_bdd["product"]["sale_price"]
	print "prix_solde_produit_en_bdd", prix_solde_produit_en_bdd
	if prix_solde_produit_en_bdd == None:
		prix_solde_produit_en_bdd = 0
		print "prix_solde_produit_en_bdd = None puis 0 "
	
	#On récupère l'ID
	id_produit_en_bdd = produit_en_bdd["product"]["id"]
	
	#Prix lu sur le site distant 
	prix_produit_distant = produit_actif.prix_produit
	print "prix_produit_distant", prix_produit_distant
	if prix_produit_distant == None:
		prix_produit_distant = 0
	
	
	#Prix solde lu sur le site distant 
	prix_solde_produit_distant = produit_actif.prix_special_produit
	print "prix_solde_produit_distant", prix_solde_produit_distant
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

def comparaison_du_produit(numero_du_produit):

	produit_actif.reinit()
	
	# Tout d'abord on lit le produit dans la BdD
	x1="products/"
	y1=str(numero_du_produit)
	z1=x1+y1
	
	try:
		produit_dans_la_bdd=wcapi.get(z1).json()
	except:
		print "Erreur de lecture de la BDD en local"
		return
		
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

	#On récupère la categorie
	categorie_produit_en_bdd = produit_dans_la_bdd["product"]["categories"][0]
	slug_categorie_produit_en_bdd = search_woocommerce_category_slug(liste_des_categories, categorie_produit_en_bdd)
	print "categorie_produit_en_bdd", categorie_produit_en_bdd


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
		destruction_enregistrement_bdd(numero_du_produit, 1)
		return

	data = html.content
	bsObj = BeautifulSoup(data)

	for x in bsObj.findAll('script'):
		bsObj.script.extract()
	for x in bsObj.findAll('noscript'):
		bsObj.noscript.extract()
	

	site_etudie = Site()
	# print "slug : ", slug_categorie_produit_en_bdd
	site_etudie.creation(slug_categorie_produit_en_bdd)
	
	
	get_GenericProduct(bsObj, site_etudie, url_produit_dans_la_bdd)

	#print "Produit : " 
	#print numero_du_produit
	if comparaison_du_nom(titre_produit_en_bdd) :
		compareprix = comparaison_du_prix(prix_produit_en_bdd) 
		if compareprix == True:
			print "Produit identique", titre_produit_en_bdd
		
		else:
			print "Prix différent : "
			print prix_produit_en_bdd
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
					destruction_enregistrement_bdd(numero_du_produit, 1)
					#memorisation_modifications(cnx, produit_dans_la_bdd, 5)
				
					try:
						#JBS le 28/9/2016
						#print(wcapi.put(z1, data_product).json())
						storeProduitActif(wcapi, categorie)
						#print "Non "
					except:
						return
					
					#maj du produit sur les-bougies.com 
					try:
						#JBS le 28/9/2016
						#print(wcapi2.put(z1, data_product).json())
						storeProduitActif(wcapi2, categorie)
						#print "Non "
					except:
						return
					
					
					memorisation_modifications(cnx, produit_dans_la_bdd, 2)
			
			else:
				print "Pb sur les prix : "
				print titre_produit_en_bdd
				print produit_actif.nom_produit
				destruction_enregistrement_bdd(numero_du_produit, 1)
				memorisation_modifications(cnx, produit_dans_la_bdd, 5)

				
				
			produit_actif.reinit()

	
	else:
		print "Titre different : "
		print titre_produit_en_bdd
		print produit_actif.nom_produit
		destruction_enregistrement_bdd(numero_du_produit, 1)
		
		memorisation_modifications(cnx, produit_dans_la_bdd, 3)
		print "DELETE Titre different :  "
	
	
	

# Ensuite on compare le titre, le prix, la description
# Et si il y a un changement, on met à jour les données
# Sinon on ne fait rien


i = 0
longueur_list = len(lines)
cnx = cnx_mysql()

#fichier_produits_modifies = open("produitsmodifies.txt", "a")


while i < longueur_list:
	n=re.findall("\d*", lines[i])
	x=n[1]
	y=int(x)
	print "i : ",i, "y : ", y
	comparaison_du_produit(y)
	i = i +1

cnx.close()

#JBS le 28/9/2016
liste_produits.store_ProduitListe(wcapi)
liste_produits.store_ProduitListe(wcapi2)

#liste_produits.store_ProduitListe(wcapi)
#fichier_produits_modifies.close()
	
	
