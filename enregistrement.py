# -*- coding: utf-8 -*-
import json
from woocommerce import API
import re
import io
from tools_moteur import *
import urllib
import os
from urlparse import urlparse
import paramiko
from PIL import Image
import requests
from StringIO import StringIO
import os

#----------------------------------------------------------------------------------------------
# Fonction qui essaie d'enregistrer le produit lorsqu'il y a eu échec à cause de l'image
# JBS le 5/10/2017
def enregistrement2meChance(w, x, wcapi):

	print w['code']
					
	# Erreur de lecture 
	# En cours de révision
	if ( w['code']=="woocommerce_product_image_upload_error") :
		print "Dans le cas : woocommerce_product_image_upload_error" 
		img=x["images"][0]["src"]
		print img
				
		img2 = requests_my_image(img)
		print "Fichier image : ", img2
		if ( img2 != False) :
			x["images"][0]["src"] = img2
			print x
			w = wcapi.post("products", x).json()

	return

#----------------------------------------------------------------------------------------------
# Fonction qui lit une image dont on a l'URL et la sauvegarde dans le dossier
# Voir : https://gist.github.com/hanleybrand/4221658
# JBS le 27/9/2017

def requests_my_image(file_url):

	print "requests_my_image" 
	suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg']
	d="/Applications/MAMP/htdocs/bougies-parfumes-oqb.fr/tmp/"
	h="http://localhost:8888/bougies-parfumes-oqb.fr/tmp/"
	
	file_name =  urlparse(file_url)[2].split('/')[-1]
	print "File Name : ", file_name
	
	file_suffix = file_name.split('.')[1]
	print "File Suffix : ", file_suffix
    
    # Je veux un seul nom de fichier image, toujours le même
    #file_name = "tmp"+"."+ file_suffix
    
	i = requests.get(file_url)
	print "i = ",i
    
	d_file_name=d+file_name
    
	if file_suffix in suffix_list and i.status_code == requests.codes.ok:
		with open(d_file_name, 'wb') as file:
			file.write(i.content)
			return(h+file_name)
 	
	else:
 		return False
        

#----------------------------------------------------------------------------------------------
#fonction qui convertit un prix avec symbole en un nombre
def convert_string_to_float(s):

	z = 0
	
		
	if s!= None and s != "":
		if s.isdigit():
			z=float(s)
		else:
		
			#JBS le 19/9/2017
			#cas particulier de la FNAC
			if type(s) == type(unicode()):
				t=s.encode('utf8')
				#On supprime Euro si ça existe
				s=t.replace("\xe2\x82\xac",",")
			
			#JBS le 2/12/2016
			#cas particulier où on a un prix de la forme 1.490,00 €					
			virguletpoint=re.search("(\d)+,(\d)+.(\d)+",s)
			if virguletpoint!= None:
				t=virguletpoint.group(0)
				s = t.replace(",", "")
				
			
			s=s.replace(",",".")
			
			#Modification le 6/10/2016 pour Sia
			k1=re.search("H(\d)+((.)?|(,)?)(\d)+",s)
			if k1!= None:
				k2=k1.group(0)
				s=s.replace(k2,"")
				
			
			#Modification le 16/3/2016
			# x=re.findall("\d+[\.?|\,?]\d+",s)
			x=re.search("(\d)+((.)?|(,)?)(\d)+",s)
			#if len(x) >0:
				#y=x[0]
				#z=float(y)
				
			#Modification le 16/3/2016	
			if x!= None:
				y=x.group(0)
				z=float(y)
				
	#print "Nombre calculé : ", z
	return z

# par defaut la version API REST utilisee est le v3 mais la v3 n'est pas la derniere des versions
# la derniere des versions est Setup for the new WP REST API integration (WooCommerce 2.6 or later)
# https://pypi.python.org/pypi/WooCommerce
# Le problème est que cette version differe sur de nombreux points avec la version v3 notamment sur les parametres
# il serait pourtant ideal de migrer vers la "wc/v1

def initBDD():
	print "initBDD"
	wcapi = API(
	#url="http://localhost:8888/bs4",
	#consumer_key="ck_6d2694abe7dfcfa2326c8d0f6153ed078a5923fb",
	#consumer_secret="cs_8afd0317af477c088784b28d712507257c9170a0"
	url="http://localhost:8888/bougies-parfumes-oqb.fr/",
	consumer_key="ck_a1256f289a64e0039eee287630163b3f10af349c",
	consumer_secret="cs_8cac616f9cb7f5031b998fb6c95151d626b4d3b1",
	timeout=30
	#Ajoute suite a qq problemes avec tendances du monde
	#JBS le 13/12/2016 - upgrade du package woocommerce python et ajout des lignes ci-dessous
	#wp_api=True, 
	#version="wc/v1"
	)	
	return wcapi	

# https://pypi.python.org/pypi/WooCommerce

def initBDD_2():
	print "initBDD_2"
	wcapi = API(
	#url="http://localhost:8888/bs4",
	#consumer_key="ck_6d2694abe7dfcfa2326c8d0f6153ed078a5923fb",
	#consumer_secret="cs_8afd0317af477c088784b28d712507257c9170a0"
	url="http://localhost:8888/bougies-parfumes-oqb.fr/",
	consumer_key="ck_a1256f289a64e0039eee287630163b3f10af349c",
	consumer_secret="cs_8cac616f9cb7f5031b998fb6c95151d626b4d3b1",
	timeout=30,
	#Ajoute suite a qq problemes avec tendances du monde
	#JBS le 13/12/2016 - upgrade du package woocommerce python et ajout des lignes ci-dessous
	wp_api=True, 
	version="wc/v2"
	)	
	return wcapi	
	
# ------------------------------------------------------------------------------------------------------------
# INITBDDREMOTE
# ------------------------------------------------------------------------------------------------------------	
# Ajout JBS le 7 juin 2016

def initBDDremote():
	print "initBDDremote"
	wcapi2 = API(
	url="http://www.les-bougies.com/",
	consumer_key="ck_a1256f289a64e0039eee287630163b3f10af349c",
	consumer_secret="cs_8cac616f9cb7f5031b998fb6c95151d626b4d3b1",
	#JBS le 12/1/2017 si je n'augmente pas la durée du timer (5 par défaut) ça plante parfois
	timeout=30
	#JBS le 13/12/2016 - upgrade du package woocommerce python et ajout des lignes ci-dessous
	#wp_api=True, 
	#version="wc/v1"
	# version = 'v2'
	)	
	return wcapi2	
	
	
def initBDDremote_2():
	print "initBDDremote_2"
	wcapi2 = API(
	url="http://www.les-bougies.com/",
	consumer_key="ck_a1256f289a64e0039eee287630163b3f10af349c",
	consumer_secret="cs_8cac616f9cb7f5031b998fb6c95151d626b4d3b1",
	#JBS le 12/1/2017 si je n'augmente pas la durée du timer (5 par défaut) ça plante parfois
	timeout=30,
	#JBS le 13/12/2016 - upgrade du package woocommerce python et ajout des lignes ci-dessous
	wp_api=True, 
	version="wc/v2"
	)	
	return wcapi2	

# ------------------------------------------------------------------------------------------------------------
# CHECK SI ON ANALYSE POUR LE LOCAL
# ------------------------------------------------------------------------------------------------------------	
def check_si_traitement_local(wcapi):
	return (wcapi.url=="http://localhost:8888/bougies-parfumes-oqb.fr/")

	
	
def createLinkUrlProduit(url):
	str = ""
	if (url != None) & (url != ""):
		str1 = '\n<a href="'
		str2 = '">Lien vers le site</a> \n'
		str = str1 + url + str2
	
	return str



# ------------------------------------------------------------------------------------------------------------
# PUT_ACCENTS
# ------------------------------------------------------------------------------------------------------------	

def put_accents(chaine):
	y=chaine.encode('utf-8')
	z=y.decode('utf-8').encode('latin1')
	w=unicode(z, "utf-8")
	return w



# ------------------------------------------------------------------------------------------------------------
# CREATE_DATA_WOOCOMMERCE seulement pour la maj d'un produit
# ------------------------------------------------------------------------------------------------------------	

def create_data_4woocommerce():
	
	#Modification JBS le 19/9/2016
	#produit_actif.prix_ancien_produit = max(produit_actif.prix_produit, produit_actif.prix_ancien_produit)
	#print "produit_actif.prix_special_produit", produit_actif.prix_special_produit
	#produit_actif c'est le produit qui est lu sur le site distant
	#on lit trois valeurs : la première prix_produit est en Read Only, la deuxième est le prix normal, la troisième le prix soldé
	#lorsqu'on stocke les données il ne faut pas de valeur à 0 mais à None
	
	#le prix soldé
	if produit_actif.prix_special_produit == 0:
		produit_actif.prix_special_produit = None
	
	#si le prix soldé et le prix régulier sont identiques
	#ce n'est pas soldé dans ce cas
	if produit_actif.prix_special_produit == produit_actif.prix_ancien_produit:
		produit_actif.prix_special_produit = None
	
	print "produit_actif.prix_produit", produit_actif.prix_produit
	print "produit_actif.prix_ancien_produit", produit_actif.prix_ancien_produit
	print "produit_actif.prix_special_produit", produit_actif.prix_special_produit
	
			
	data = {}
	data = {
		"product": {
			#JBS le 22/9/2016 - inutile car le titre est necessairement identique
			#"title": produit_actif.nom_produit,
			#"type": "simple",
			
			#JBS le 22/9/2016 - ce champ est Read Only
			#"price": produit_actif.prix_produit,
			
			"regular_price": produit_actif.prix_ancien_produit,
			"sale_price": produit_actif.prix_special_produit,
			 #"description": produit_actif.url_produit,
			 #"description": createLinkUrlProduit(produit_actif.url_produit) + produit_actif.description_produit,
			 #"enable_html_description":True,
			 #"enable_html_short_description":True,

			 #"categories": [categorie],
			 #"images": [
			 	#{
			 		#"src": produit_actif.url_image_produit,
			 		#"position": 0
			 	#}
			 #]
		}
	}
	
	#On ne stocke que s'il y a un nom, une URL, une image et un prix
	if produit_actif.nom_produit != "":
		if produit_actif.prix_produit != None:
			#print data
  			return(data)


	return(None)

# ------------------------------------------------------------------------------------------------------------
# STOCKAGE_IMAGE_REMOTE
#
# ------------------------------------------------------------------------------------------------------------
def stockage_image_en_remote():
	print "Cas particuler Historiae / Ejea"
	
	# u : URL de l'image distante du site exploré
	u=produit_actif.url_image_produit
	print "URL origine", u
	
	# f : non du fichier image
	parsed_url = urlparse(u)
	p=parsed_url.path
	f=os.path.basename(p)
	
	# newurl = URL sur le site distant les-bougies.com 	
	newurl="vhosts/www.les-bougies.com/htdocs/tmp/"+f
	print "URL image distante : ", newurl

	# Creation dun objet ftp pour ecriture sur le distant
	host = "sftp.dc0.gpaas.net" # Gandi
	port = 22
	username = "3166695"
	password = "142857JBSjbs1"
	transport = paramiko.Transport(host, port)
	transport.connect(username = username, password = password)
	
	sftp = paramiko.SFTPClient.from_transport(transport)
	
	# Recuperation de l'image sur le site explore (on effectue la requete en local)
	# Stockage en local de l'image
	# dir_local='tmpimages/'+f
		
	response = requests.get(u)
	img = Image.open(StringIO(response.content))
	dir_local = 'tmpimages/'+"avirer."+img.format
	print "Dossier image locale : ", dir_local
	
	img.save(dir_local)
	
	
	# Stockage en remote
	sftp.put(dir_local,newurl)

# ------------------------------------------------------------------------------------------------------------
# CHANGE_URL_IMAGE_PRODUIT
#
# ------------------------------------------------------------------------------------------------------------
# On est dans le cas où on fait des sauvegardes sur le site distant
# On a fait aupravant un enregistrement sur le site local
# Les images sont déjà stockées sur notre serveur
# On subsititue à l'URL de l'image du produit en lecture l'URL présente sur notre site

def change_url_image_produit():

	u=produit_actif.url_image_produit
	print "URL origine", u
	parsed_url = urlparse(u)
	p=parsed_url.path
	f=os.path.basename(p)
	
	newurl="http://www.les-bougies.com/tmp/"+f
	print "Nouvelle URL Image : ", newurl
	return newurl
	


# ------------------------------------------------------------------------------------------------------------
# CHANGE_URL_IMAGE_PRODUIT_HTTPS_HTTP
#
# ------------------------------------------------------------------------------------------------------------
# On est dans le cas tendances-du-monde
# L'image indiquée est en HTTP mais il y a un moved permanently en HTTPS

def change_url_image_produit_https_http():

	u=produit_actif.url_image_produit
	print "URL origine", u
	parsed_url = urlparse(u)
	
	newurl= "https"+"://"+parsed_url.netloc+parsed_url.path+parsed_url.params+parsed_url.query+parsed_url.fragment
	print "Nouvelle URL Image : ", newurl
	return newurl
	
	

# ------------------------------------------------------------------------------------------------------------
# STORE_PRODUIT_ACTIF
# ------------------------------------------------------------------------------------------------------------	
# Exemple de data pour la nouvelle version de l'API REST Woocommerce 
# {'description': 'Un subtil parfum de pamplemousse', 'regular_price': '45.0', 
# 'short_description': 'Bougie Parfumee Platinum Max One Baobab', 
# 'images': [{
	#'src': 'http://cdn.mise-en-scene.com/media/catalog/product/cache/4/image/363x/040ec09b1e35df139433887a97daa66f/b/o/bougie_parfum_e_max_one_platinum_baobab_collection.jpg', 
	#'position': 0}], 
# 'type': 'simple', 
#'categories': [{'id': 116}], 
# 'name': 'Bougie Parfumee Platinum Max One Baobab - Mise en scene Belgique'}


def storeProduitActif(wcapi, categorie):
	#Dictionaries are created using the curly braces. 
	produit_actif.prix_ancien_produit = max(produit_actif.prix_produit, produit_actif.prix_ancien_produit)
	
	
	if produit_actif.prix_special_produit == 0:
		produit_actif.prix_special_produit = None
	#ce n'est pas soldé dans ce cas
	if produit_actif.prix_special_produit == produit_actif.prix_ancien_produit:
		produit_actif.prix_special_produit = None	
		
	#JBS le 17/3/2017
	# Cas particulier Historiae (28) et Ejea (156)
	# Ces sites refusent les robots - mon IP est interdite
	# Par contre en accedant à partir de mon local c'est OK
	# Je me deboruille de la façon suivante :
	# Je lis en local, je stocke l'image en remote et lorsque je lis en remote je prends l'image stockee lors de la lecture en local

		
	if (categorie == '28') or (categorie == '156') :
		print "La categorie est : ", categorie
		# Si on enregistre en local
		if check_si_traitement_local(wcapi):
			stockage_image_en_remote() 
		# Si on enregistre en remote
		else:
			print "Enregistrement en remote : image : "
			produit_actif.url_image_produit = change_url_image_produit()
	
	# tendances-du-monde
	# ça ne suffit pas de rempalcer http par https
	# j'ai toujours l'erreur woocommerce_product_image_upload_error
	
	# if (categorie == '186') :						
		# produit_actif.url_image_produit = change_url_image_produit_https_http()
		
								
	data = {}
	
	# pour la version legacy de BS 4
	# Version OBSOLETE
	
	'''
	data = {
		"product": {
			"title": produit_actif.nom_produit,
			#"name": produit_actif.nom_produit,
			"type": "simple",
			"price": produit_actif.prix_produit,
			"regular_price": produit_actif.prix_ancien_produit,
			 "sale_price": produit_actif.prix_special_produit,
			 #"description": produit_actif.url_produit,
			 "description": createLinkUrlProduit(produit_actif.url_produit) + produit_actif.description_produit,
			 "enable_html_description":True,
			 "enable_html_short_description":True,

			 "categories": [categorie],
			 "images": [
			 	{
			 		"src": produit_actif.url_image_produit,
			 		#"src": "http://www.scandles.fr/wp-content/uploads/2015/10/bougie-black_trompette_anges_10oz-510x600.jpg",
			 		"position": 0
			 	}
			 ]
		}
	}
	'''
	
	# Pour BS 4 v3.0
	# JBS le 7/4/2017
	data = {
		# "title": produit_actif.nom_produit,
		"name": produit_actif.nom_produit,
		"type": "simple",
		#"price": produit_actif.prix_produit,
		"regular_price": str(produit_actif.prix_ancien_produit),
		"sale_price": str(produit_actif.prix_special_produit),
		#"description": produit_actif.url_produit,
		"description": createLinkUrlProduit(produit_actif.url_produit) + produit_actif.description_produit,
		"enable_html_description":True,
		"enable_html_short_description":True,

		"categories": [
			{
				"id": categorie
			}
		],
		
		"images": [
			{
			 	"src": produit_actif.url_image_produit,
			 	#"src": "http://www.scandles.fr/wp-content/uploads/2015/10/bougie-black_trompette_anges_10oz-510x600.jpg",
			 	"position": 0
			 }
		]
	}
	
	#On ne stocke que s'il y a un nom, une URL, une image et un prix
	if produit_actif.nom_produit != "":
		if produit_actif.url_produit != "":
			if produit_actif.prix_produit != None:
				if produit_actif.url_image_produit != "":
					print data
					
					
							
  					liste_produits.ajout_ProduitListe(data)





# ------------------------------------------------------------------------------------------------------------
# MAJ_PRODUIT_ACTIF
# ------------------------------------------------------------------------------------------------------------	
# Exemple de data pour la nouvelle version de l'API REST Woocommerce 
# {'description': 'Un subtil parfum de pamplemousse', 'regular_price': '45.0', 
# 'short_description': 'Bougie Parfumee Platinum Max One Baobab', 
# 'images': [{
	#'src': 'http://cdn.mise-en-scene.com/media/catalog/product/cache/4/image/363x/040ec09b1e35df139433887a97daa66f/b/o/bougie_parfum_e_max_one_platinum_baobab_collection.jpg', 
	#'position': 0}], 
# 'type': 'simple', 
#'categories': [{'id': 116}], 
# 'name': 'Bougie Parfumee Platinum Max One Baobab - Mise en scene Belgique'}


def majProduitActif(wcapi, categorie, numero_du_produit):
	#Dictionaries are created using the curly braces. 
	produit_actif.prix_ancien_produit = max(produit_actif.prix_produit, produit_actif.prix_ancien_produit)
	
	
	if produit_actif.prix_special_produit == 0:
		produit_actif.prix_special_produit = None
	#ce n'est pas soldé dans ce cas
	if produit_actif.prix_special_produit == produit_actif.prix_ancien_produit:
		produit_actif.prix_special_produit = None	
		
	#JBS le 17/3/2017
	# Cas particulier Historiae (28) et Ejea (156)
	# Ces sites refusent les robots - mon IP est interdite
	# Par contre en accedant à partir de mon local c'est OK
	# Je me deboruille de la façon suivante :
	# Je lis en local, je stocke l'image en remote et lorsque je lis en remote je prends l'image stockee lors de la lecture en local

	if (categorie == '28') or (categorie == '156') :
		print "La categorie est : ", categorie
		# Si on enregistre en local
		if check_si_traitement_local(wcapi):
			stockage_image_en_remote() 
		# Si on enregistre en remote
		else:
			print "Enregistrement en remote : image : "
			produit_actif.url_image_produit = change_url_image_produit()


	# Cas Le Bazaristain - JBS le 26/9/2017					
	#if (categorie == '92') :
		#print "Le Bazaristain "
		#img = requests_image(file_url) 
		#if (img != False) :
			#print "Image : ", img
			#produit_actif.url_image_produit = img	
							
	data = {}
	
	# pour la version legacy de BS 4
	
	# Pour BS 4 v3.0
	# JBS le 7/4/2017
	data = {
		# title n'existe pas dans la version de cette API
		# "title": produit_actif.nom_produit,
		# Le nom reste le même
		#"name": produit_actif.nom_produit,
		# type ne sert pas
		#"type": "simple",
		#"price": produit_actif.prix_produit,
		"regular_price": str(produit_actif.prix_ancien_produit),
		"sale_price": str(produit_actif.prix_special_produit),
		#"description": produit_actif.url_produit,
		# si la description change on supprime
		#"description": createLinkUrlProduit(produit_actif.url_produit) + produit_actif.description_produit,
		#"enable_html_description":True,
		#"enable_html_short_description":True,

		#"categories": [
			#{
				#"id": categorie
			#}
		#],
		
		#"images": [
			#{
			 	#"src": produit_actif.url_image_produit,
			 	#"src": "http://www.scandles.fr/wp-content/uploads/2015/10/bougie-black_trompette_anges_10oz-510x600.jpg",
			 	#"position": 0
			# }
		#]
	}
	
	x1="products/"
	y1=str(numero_du_produit)
	z1=x1+y1
	
	print "MAJ du Produit : ", numero_du_produit
	print(wcapi.put(z1, data).json())


# ------------------------------------------------------------------------------------------------------------
# CLASS JsonWoocommerceProduit
# ------------------------------------------------------------------------------------------------------------	


class JsonWoocommerceProduit:
	'Produit Woocommerce'
	def __init__(self):
		self.title=""
		self.type="simple"
		self.price = 0
		self.regular_price=0
		self.sale_price=0
		self.description = ""
		self.enable_html_description = True
		self.enable_html_short_description = True
		self.categories = [0]
		self.src = ""
		self.position = 0
	
	def create_Produit(self, title, price, regular_price, sale_price, description, categories, src):
		self.title=title
		self.type="simple"
		self.price = price
		self.regular_price=regular_price
		self.sale_price=sale_price
		self.description = description
		self.enable_html_description = True
		self.enable_html_short_description = True
		self.categories = [categories]
		self.src = src
		
	def printProduit(self):
		if self.title != "":
			print self.title
		if self.price != 0:
			print self.price
		if self.regular_price != 0:
			print self.regular_price
		if self.sale_price != 0:
			print self.sale_price
		if self.description != "":
			print self.description
		if self.src != "":
			print self.src
		print self.categories


# ------------------------------------------------------------------------------------------------------------
# CLASS JsonWoocommerceListeProduit
# ------------------------------------------------------------------------------------------------------------	
		

class JsonWoocommerceListeProduit:
	'Liste des Produit Woocommerce'		
	def __init__(self):
		self.listeDesProduits=[]
		self.nomDesProduits=[]
		
	def ajout_ProduitListe(self, produit):
		# pour la version BS4 v3
		titre_du_produit = produit["name"]
		#titre_du_produit = produit["product"]["title"]
		longeur_de_la_liste = len(self.nomDesProduits)
		deja_dans_la_liste = False
		
		if longeur_de_la_liste >0:
			deja_dans_la_liste = titre_du_produit in self.nomDesProduits
			print "Longueur de la liste : "
			print longeur_de_la_liste
			print "deja_dans_la_liste"
			print deja_dans_la_liste
			print titre_du_produit
			
		if not deja_dans_la_liste:	
			self.listeDesProduits.append(produit)	
			self.nomDesProduits.append(titre_du_produit)
				
	def print_ProduitListe(self):
		i = 1
		for x in self.listeDesProduits:
			print "produit : "
			print i
			i = i +1
			x.printProduit()	
			
	def store_ProduitListe(self, wcapi):
		i = 1
		#d = {}
		for x in self.listeDesProduits:
			print "store produit : "
			#d={"product":{}}
			#d['product']=x
			print i
			i = i +1
			print x
			w = wcapi.post("products", x).json()
			
		return
				
				
	def vide_ProduitListe(self):
		self.listeDesProduits=[]
		self.nomDesProduits=[]

# ------------------------------------------------------------------------------------------------------------
# CLASS Produit
# ------------------------------------------------------------------------------------------------------------	

class Produit:
	'Enregistrement en cours'
	def __init__(self):
		self.nom_produit=""
		self.prix_produit=None
		self.prix_ancien_produit = None
		self.prix_special_produit=None
		self.url_image_produit=""
		self.url_produit = ""
		self.description_produit = ""
		self.categorie = 0
	
	def reinit(self):
		self.nom_produit=""
		self.prix_produit=None
		self.prix_ancien_produit = None
		self.prix_special_produit=None
		self.url_image_produit=""
		self.url_produit = ""
		self.description_produit = ""
		self.categorie = 0
		
	
		
			
	def printProduit(self):
		if self.nom_produit != "":
			print self.nom_produit
		if self.prix_produit != None:
			print self.prix_produit
		if self.prix_ancien_produit != None:
			print self.prix_ancien_produit
		if self.prix_special_produit != None:
			print self.prix_special_produit
		if self.url_image_produit != "":
			print self.url_image_produit
		if self.url_produit != "":
			print self.url_produit
		if self.description_produit != "":
			print self.description_produit

	def add_NomProduit(self, nom_produit):
		self.nom_produit = nom_produit


	def add_UrlProduit(self, url_produit):
		self.url_produit = url_produit
		
	def add_UrlImageProduit(self, url_image_produit):
		self.url_image_produit = url_image_produit
	
	#Modification importante le 11 mars 2016	
	def add_PrixProduit(self, prix_produit, prix_ancien_produit, prix_special_produit):
		prix_readonly = convert_string_to_float(prix_produit)
		prix_regulier = convert_string_to_float(prix_ancien_produit)
		prix_promo = convert_string_to_float(prix_special_produit)	
		
		if (prix_promo > prix_regulier):
			x = prix_promo
			prix_promo = prix_regulier
			prix_regulier = x
			
		self.prix_produit = prix_readonly
		self.prix_ancien_produit = prix_regulier
		self.prix_special_produit = prix_promo	
		
		#self.prix_produit = min(prix_readonly, prix_regulier, prix_promo)
		#self.prix_ancien_produit = max(prix_readonly, prix_regulier, prix_promo)
		#self.prix_special_produit = max(prix_readonly, prix_regulier, prix_promo)	
		
				
	
	def add_Description_Produit(self, description):
		self.description_produit = description
		
	def add_Categorie_Produit(self, categorie):
		#print categorie
		self.categorie = int(categorie)

			



global produit_actif
produit_actif = Produit()
global data_file
data_file=open("data.txt","w")

global produit_courant
produit_courant = JsonWoocommerceProduit()

global liste_produits
liste_produits = JsonWoocommerceListeProduit()

