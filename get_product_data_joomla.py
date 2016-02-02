# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from enregistrement import *
from get_product_data_magento import *


#---------------------------------------------------------------------------------
#on cherche l'URL de l'image
def give_JoomlaProductImgURL(bsObj):

#La Lumiere des Fees
	image=bsObj.find("meta",{"property":"og:image"})
	if image != None:
		#print "Cas 1 image"
		imgUrlSrc = image["content"]
		if imgUrlSrc != "":
			return imgUrlSrc

	return ""


#----------------------------------------------------------------------------------------------
#fonction qui verifie que la page Joomla est celle d'un produit	
def check_JoomlaIsItAproduct(bsObj):
	
	produit = bsObj.find("div", {"id":"hikashop_product_right_part"})
	return produit
	

#---------------------------------------------------------------------------------
#on cherche le nom du produit Joomla
def give_JoomlaProductName(bsObj, produit):

	produit_title = bsObj.find("title")
	if produit_title != None:
		nom_produit = produit_title.get_text()
		#print nom_produit
		if est_ce_une_bougie(nom_produit):
			return(nom_produit)
	
					
	return ""

#---------------------------------------------------------------------------------
#cherche le prix d'un produit Woocommerce Wordpress
def check_JoomlaProductPrice(bsObj):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	

	#1er cas La lumiere des Fees
	#Si pas de soldes, alors un seul prix
	prix = bsObj.find("span",{"class":"hikashop_product_price"})
	if prix != None:
		prixTxt = prix.get_text()


	#Si on a prix soldé	
	prix_solde=bsObj.find("span",{"class":"hikashop_product_price_with_discount"})
	
	if prix_solde != None:
		special_prixValueTxt = prix_solde.get_text()
		#print old_prixValueTxt
			
		#On a un ancien prix et un prix affiché
		#Le prix affiché est alors le prix soldé
		#et l'ancien prix le prix d'origine
		ancien_prix = bsObj.find("span",{"class":"hikashop_product_price_before_discount"})
		if ancien_prix != None:
			#Le prix soldé est le prix affiché
			old_prixValueTxt = ancien_prix.get_text()
			
			#l"ancien prix est le prix
				
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)


#---------------------------------------------------------------------------------
#Retourne la description du produit
#On sait ici que la page est une celle du produit - il y a un prix - un nom
def get_JoomlaProductDescription(bsObj):

	#Durance
	str = ""
	description=bsObj.find("div", {"id":"description"})
	if description != None:
		str = get_MagentoProductDescriptionExtractStr(bsObj, description)
		return str
	
						
	#return str 
	

#---------------------------------------------------------------------------------	
def get_JoomlaProduct(bsObj):

	produit = check_JoomlaIsItAproduct(bsObj)			
	if produit != None: 
	
		#on teste si c'est une bougie
		nom_produit = give_JoomlaProductName(bsObj, produit)
		if (nom_produit != "") & (nom_produit != None):
			produit_actif.add_NomProduit(nom_produit)
			
			print nom_produit	
			print "On cherche le prix"	
			
			prix, old_price, special_price = check_JoomlaProductPrice(bsObj)
			
			if prix != None: 
				print prix
				produit_actif.add_PrixProduit(prix, old_price, special_price)
				imgUrlSrc = give_JoomlaProductImgURL(bsObj)
				if imgUrlSrc != "":
					#print imgUrlSrc
					produit_actif.add_UrlImageProduit(imgUrlSrc)
					
					description=get_JoomlaProductDescription(bsObj)
					produit_actif.add_Description_Produit(description)

