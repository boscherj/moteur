# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from enregistrement import *


#---------------------------------------------------------------------------------
#on cherche l'URL de l'image
def give_PrestashopProductImgURL(bsObj):

#La boite a bougies
	image=bsObj.find("img", {"id":"bigpic"})
	if image != None:
		#print "Cas 1 image"
		imgUrlSrc = image['src']
		return imgUrlSrc
				

	return ""


#---------------------------------------------------------------------------------
#on cherche le nom du produit 
def give_PrestashopProductName(bsObj, produit):

	produit_title = bsObj.find("title")
	if produit_title != None:
		nom_produit = produit_title.get_text()
		#print nom_produit
		if  check_est_une_bougie_PrestaShop(bsObj):
			return(nom_produit)
		
	return ""
					
#---------------------------------------------------------------------------------
#on vérifie que c'est bien un produit Prestahop
def check_PrestahopIsItAproduct(bsObj):

	#plusieurs possibilites pour savoir si la page est un produit
	#cas 1
	produit=bsObj.find("body", {"id":"product"})
	if produit!= None: 
		print "produit"
		return produit
		
	#cas 2	
	produit= bsObj.find("div", {"class":"product_attributes"})
	if produit!= None: 
		print "produit"
		return produit

	#ce n'est pas un produit
	return produit	

#----------------------------------------------------------------------------------------------
#fonction qui verifie que la page produit  CMS PrestaShop - Woocommerce est celle d une bougie	
def check_est_une_bougie_PrestaShop(bsObj):
	
	check = False
	print "check_est_une_bougie_PrestaShop"
	#produit = bsObj.find("title")
	#nom_produit = produit.get_text()
	#if nom_produit.lower().find('bougie') >= 0:
		#print nom_produit	
		#check = True				
	nom = bsObj.find("h1", {"itemprop":"name"})
	if nom != None:
		nom_produit = nom.get_text()
		print "1er cas"
		print nom_produit
		if est_ce_une_bougie(nom_produit):
			check = True
			return check

	nom = bsObj.find("h1", {"class":"supplier_title"})	
	if nom != None:
		nom_produit = nom.get_text()
		print "2eme cas"
		print nom_produit
		if est_ce_une_bougie(nom_produit):
			check = True
			return check
	
	
	nom = bsObj.find("h1", {"class":"productTitle"})	
	if nom != None:
		nom_produit = nom.get_text()
		print "3eme cas"
		print nom_produit
		if est_ce_une_bougie(nom_produit):
			check = True
			return check

			
	return check

#---------------------------------------------------------------------------------
#cherche le prix d'un produit Prestashop
def check_PrestashopProductPrice(bsObj):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	

	#1er cas
	prix = bsObj.find("span", {"class":"our_price_display"})
	if prix != None:
		prixTxt = prix.get_text()
	
	else:
		prix = bsObj.find("p", {"class":"our_price_display"})
		if prix != None:	
			prixTxt = prix.get_text()


	#prix soldé	
	ps=bsObj.find("p", {"id":"old_price"})
	
	if ps != None:
		old_prix = ps.find("span", {"class":"price"})
		if old_prix != None:
			old_prixValueTxt = old_prix.get_text()
			#print old_prixValueTxt
			
			#On a un ancien prix et un prix affiché
			#Le prix affiché est alors le prix soldé
			#et l'ancien prix le prix d'origine
			if prix != None:
				#Le prix soldé est le prix affiché
				special_prixValueTxt = prixTxt	
				#l"ancien prix est le prix
				

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)

		
		
		
		
#---------------------------------------------------------------------------------	
def get_PrestaShopProduct(bsObj):

	print "PrestaShop"	
	produit = check_PrestahopIsItAproduct(bsObj)			
	if produit != None: 
	
		#on teste si c'est une bougie
		nom_produit = give_PrestashopProductName(bsObj, produit)
		if nom_produit != "":
			produit_actif.add_NomProduit(nom_produit)
			
			print nom_produit	
			print "On cherche le prix"	
			prix, old_price, special_price = check_PrestashopProductPrice(bsObj)
			
			if prix != None: 
				print prix
				produit_actif.add_PrixProduit(prix, old_price, special_price)
				imgUrlSrc = give_PrestashopProductImgURL(bsObj)
				if imgUrlSrc != "":
					#print imgUrlSrc
					produit_actif.add_UrlImageProduit(imgUrlSrc)
				
