# -*- coding: utf-8 -*-
import json
from woocommerce import API
import re
import io, json
from tools_moteur import *

#----------------------------------------------------------------------------------------------
#fonction qui convertit un prix avec symbole en un nombre
def convert_string_to_float(s):

	z = 0
	
		
	if s!= None and s != "":
		if s.isdigit():
			z=float(s)
		else:
			s=s.replace(",",".")
			x=re.findall("\d+[\.?|\,?]\d+",s)
			if len(x) >0:
				y=x[0]
				z=float(y)
	
	return z


def initBDD():
	wcapi = API(
	#url="http://localhost:8888/bs4",
	#consumer_key="ck_6d2694abe7dfcfa2326c8d0f6153ed078a5923fb",
	#consumer_secret="cs_8afd0317af477c088784b28d712507257c9170a0"
	
	
	url="http://localhost:8888/bougies-parfumes-oqb.fr/",
	consumer_key="ck_a1256f289a64e0039eee287630163b3f10af349c",
	consumer_secret="cs_8cac616f9cb7f5031b998fb6c95151d626b4d3b1"
	
	
	)	
	return wcapi	

def createLinkUrlProduit(url):
	str = ""
	if (url != None) & (url != ""):
		str1 = '\n<a href="'
		str2 = '">Lien vers le site</a> \n'
		str = str1 + url + str2
	
	return str


#------------------------------------------------------------------------------
# Pour l'Occitane qui utilise des accents dans ses URLs	

def put_accents(chaine):
	y=chaine.encode('utf-8')
	z=y.decode('utf-8').encode('latin1')
	w=unicode(z, "utf-8")
	return w

def storeProduitActif(wcapi, categorie):
	#Dictionaries are created using the curly braces. 
	produit_actif.prix_ancien_produit = max(produit_actif.prix_produit, produit_actif.prix_ancien_produit)
	
	
	if produit_actif.prix_special_produit == 0:
		produit_actif.prix_special_produit = None
	#ce n'est pas soldé dans ce cas
	if produit_actif.prix_special_produit == produit_actif.prix_ancien_produit:
		produit_actif.prix_special_produit = None	
		
			
	data = {}
	data = {
		"product": {
			"title": produit_actif.nom_produit,
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
			 		"position": 0
			 	}
			 ]
		}
	}
	
	#On ne stocke que s'il y a un nom, une URL, une image et un prix
	if produit_actif.nom_produit != "":
		if produit_actif.url_produit != "":
			if produit_actif.prix_produit != None:
				if produit_actif.url_image_produit != "":
		
					print data
  					#data_file.write(json.dumps(data))
  					#nom_du_produit=produit_actif.nom_produit
  					#print "nom_du_produit"
  					#print type(nom_du_produit)
  					
  					#description_du_produit = createLinkUrlProduit(produit_actif.url_produit)  + produit_actif.description_produit
  					
  					#pc=JsonWoocommerceProduit()
  					#pc.create_Produit(nom_du_produit, produit_actif.prix_produit, produit_actif.prix_ancien_produit, produit_actif.prix_special_produit, description_du_produit, [categorie], produit_actif.url_image_produit)
  					
  					#pc.printProduit()
  					
  					liste_produits.ajout_ProduitListe(data)
  					#print "Liste des produits : "
  					#liste_produits.print_ProduitListe()
					#return(wcapi.post("products", data).json())

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


		

class JsonWoocommerceListeProduit:
	'Liste des Produit Woocommerce'		
	def __init__(self):
		self.listeDesProduits=[]
		
	def ajout_ProduitListe(self, produit):
		self.listeDesProduits.append(produit)	
		
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
			print(wcapi.post("products", x).json())


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
		
	def add_PrixProduit(self, prix_produit, prix_ancien_produit, prix_special_produit):
		self.prix_produit = convert_string_to_float(prix_produit)
		self.prix_ancien_produit = convert_string_to_float(prix_ancien_produit)
		self.prix_special_produit = convert_string_to_float(prix_special_produit)
	
	def add_Description_Produit(self, description):
		self.description_produit = description
		
	def add_Categorie_Produit(self, categorie):
		print categorie
		self.categorie = int(categorie)

			



global produit_actif
produit_actif = Produit()
global data_file
data_file=open("data.txt","w")

global produit_courant
produit_courant = JsonWoocommerceProduit()

global liste_produits
liste_produits = JsonWoocommerceListeProduit()

