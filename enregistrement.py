# -*- coding: utf-8 -*-
import json
from woocommerce import API
import re



#----------------------------------------------------------------------------------------------
#fonction qui convertit un prix avec symbole en un nombre
def convert_string_to_float(s):

	z = 0
	if s!= None:
		s=s.replace(",",".")
		x=re.findall("\d+[\.?|\,?]\d+",s)
		y=x[0]
		z=float(y)
		
	return z


def initBDD():
	wcapi = API(
	url="http://localhost:8888/bs4",
	consumer_key="ck_6d2694abe7dfcfa2326c8d0f6153ed078a5923fb",
	consumer_secret="cs_8afd0317af477c088784b28d712507257c9170a0"
	)	
	return wcapi	

def storeProduitActif(wcapi, categorie):
	#Dictionaries are created using the curly braces. 
	produit_actif.prix_ancien_produit = max(produit_actif.prix_produit, produit_actif.prix_ancien_produit)
	if produit_actif.prix_special_produit == 0:
		produit_actif.prix_special_produit = None
			
	data = {}
	data = {
		"product": {
			"title": produit_actif.nom_produit,
			"type": "simple",
			"price": produit_actif.prix_produit,
			"regular_price": produit_actif.prix_ancien_produit,
			 "sale_price": produit_actif.prix_special_produit,
			 "description": produit_actif.url_produit,
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
					return(wcapi.post("products", data).json())


class Produit:
	'Enregistrement en cours'
	def __init__(self):
		self.nom_produit=""
		self.prix_produit=None
		self.prix_ancien_produit = None
		self.prix_special_produit=None
		self.url_image_produit=""
		self.url_produit = ""
	
	def reinit(self):
		self.nom_produit=""
		self.prix_produit=None
		self.prix_ancien_produit = None
		self.prix_special_produit=None
		self.url_image_produit=""
		self.url_produit = ""
		
	
		
			
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
	

global produit_actif
produit_actif = Produit()
