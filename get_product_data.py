# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *from get_product_data_magento import *
from get_product_data_prestashop import *

#Pour rappel : #Magento 1
#PrestaShop 2
#WooCommerce 3
#4Joomla 4

#---------------------------------------------------------------------------------
def get_WoocommerceWordpressProduct(bsObj):
	
	print "Woocommerce"
	
	#Il y a deux possibilites pour que ce soit une page produit
	#Soit il y a un prix dans meta itemprop
	#Soit il y a un prix dans p itemprop
	cas1 = bsObj.find("meta", {"itemprop":"price"})
	cas2 = bsObj.find("p", {"itemprop":"price"})
	
	prix_produit = None
	
	#Pour que ce soit une bougie il y a deux possibilites
	#Soit dans le titre on trouve le mot bougie
	#Soit la categorie contient le mot bougie
	
	#En resume il y a quatre cas qui marchent
	#
	
	#On sait que c est une page produit
	#On recupere le prix
	
	if cas1:
		prix_produit = cas1['content']
		print "cas 1"

	else:
		if cas2:
			prix_produit = cas2.get_text()
			print "cas 2"
		
	if prix_produit != None: 
		print "Page produit"
		nom = bsObj.find("h1", {"itemprop":"name"})
		nom_produit = nom.get_text()
		print "nom_produit"
		print nom_produit
		
		#on verifie que c est une bougie
		if check_est_une_bougie_woocommerce(bsObj):
			print(nom_produit)
			print(prix_produit) 
				
#---------------------------------------------------------------------------------
#cherche le prix d'un produit Magento
def check_MagentoProductPrice(bsObj):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#pas de prix soldé
	prix = bsObj.find("span", {"class":"price"})
	if prix != None:
		prixTxt = prix.get_text()
	
	#prix soldé	
	old_prix = bsObj.find("p", {"class":"old-price"})	
	if old_prix != None:
		old_prixValue = old_prix.find("span", {"class":"price"})
		old_prixValueTxt = old_prixValue.get_text()
		
		special_prix = bsObj.find("p", {"class":"special-price"})	
		if special_prix != None:
			special_prixValue = special_prix.find("span", {"class":"price"})
			special_prixValueTxt = special_prixValue.get_text()

	#si on touve un prix et un prix de solde différent du prix initial alors ce n'est pas le bon produit
	if prixTxt != None:
		if old_prixValueTxt != None:
			if old_prixValueTxt != prixTxt:
				print "Anomalie"
				return(prixTxt, None, None)
				
				
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)
	
#---------------------------------------------------------------------------------
def get_MagentoProductLeBonMarche(bsObj):
	
	print "Magento Le Bon Marche"
	
	produit = bsObj.find("meta", {"property":"og:type"})
	if produit != None: 
		if produit["content"] == "product":
			produit_title = bsObj.find("meta", {"property":"og:title"})
			if produit_title != None:
				nom_produit = produit["content"]
				if check_est_une_bougie_Magento(bsObj):
					print(nom_produit)
			
				#ce n'est pas une bougie				
				else:
					print "Pas une bougie"	
					return
			else:
				print "Pas de titre"
		else:
			print "Pas un produit"
			return
	else:
		return

	
	
	#L'image
	i=bsObj.find("meta", {"property":"og:image"})
	if i!= None:
		print i["content"]	
			
	price, old_price, special_price = check_MagentoProductPrice(bsObj)
	if price != None:
			print "Price"
			print price
			
	if old_price != None:
		print "Old price"
		print old_price
			
	if special_price != None:
		print "Special price"
		print special_price
	
#---------------------------------------------------------------------------------
def get_MagentoProductDiptyqueparis(bsObj):
	
	print "Magento Diptyqueparis"
	
	produit = bsObj.find("div", {"class":"product-shop details details-top"})
	if produit != None: 
		nom_produit = produit.h3.get_text()
		#on teste si c'est une bougie
		if check_est_une_bougie_Magento(bsObj):
			print(nom_produit)
			
		#ce n'est pas une bougie				
		else:
			print "Pas une bougie"	
			return

	prixProduit = bsObj.find("div", {"class":"product"})
	if prixProduit != None: 
		x=bsObj.find("div", {"class":"features-holder"})
		if x != None:
			y=x.find("div", {"id":"candle-care-div"})
			if y != None: 
				z=y.find_next_siblings("strong")
				if z != None:
					print "Prix du produit Diptyqueparis"
					print z[0].get_text()

	else:
		return
		#je ne m'occupe pas des soldes pour l'instant
	
	
	#L'image
	i=bsObj.find("img", {"id":"large-image"})
	if i!= None:
		print i["src"]	
			


#---------------------------------------------------------------------------------
def ex_get_MagentoProduct(bsObj):
	
	print "Magento"
	
	produit = bsObj.find("li", {"class":"product"})
	if produit != None: 
		print "Produit"
		price, old_price, special_price = check_MagentoProductPrice(bsObj)
		
		if price != None:
			print "Price"
			print price
			
		if old_price != None:
			print "Old price"
			print old_price
			
		if special_price != None:
			print "Special price"
			print special_price
		
		
		
		prix = bsObj.find("span", {"class":"price"})
		if prix != None: 
			print "Il y a un prix"
			nom_produit = produit.get_text()
			
			#on teste si c'est une bougie
			if check_est_une_bougie_Magento(bsObj):
				print(nom_produit)
				print(prix.get_text()) 
				
				#durance
				image=bsObj.find("div", {"class":"product-image-gallery"})
				if image != None:
					print "Cas 1 image"
					imgUrlSrc = image.img['src']
					print imgUrlSrc
				
				else:
					#esteban
					image=bsObj.find("p", {"class":"main-product-img"})
					if image != None:
						print "Cas 2 image"
						imgUrlSrc = image.a["href"]
						print imgUrlSrc
						
					else:
						#synopsisparis
						image=bsObj.find("div", {"class":"product-img-box"})
						if image != None:
							print "Cas 3 image"
							imgUrlSrc = image.img["src"]
							print imgUrlSrc
			
			#ce n'est pas une bougie				
			else:
				print "Pas une bougie"	
				
								
#---------------------------------------------------------------------------------
#La lumiere des fees
def get_JoomlaProduct(bsObj):
	
	print "Joomla"
	produit = bsObj.find("div", {"id":"hikashop_product_right_part"})
	if produit != None: 
		titre = bsObj.find("title")
		if titre != None: 
			nom_produit = titre.get_text()
			prix = bsObj.find("span", {"class":"hikashop_product_price_with_discount"})

			if nom_produit.lower().find('bougie') >= 0:
				print(nom_produit)
			if prix != None:
				print (prix)
	
#---------------------------------------------------------------------------------
	
def getproductData(bsObj, cms):	if cms==1:	
		#Magento
		get_MagentoProduct(bsObj)
		
	elif cms==2:
		#PrestaShop
		get_PrestaShopProduct(bsObj)
		
	elif cms==3:
	#Woocommerce Wordpress
		get_WoocommerceWordpressProduct(bsObj)
		
	elif cms==4:
	#Jommla
		get_JoomlaProduct(bsObj)
		
	elif cms==5:
	#Magento Diptyqueparis
		#get_MagentoProductDiptyqueparis(bsObj)
		get_MagentoProduct(bsObj)
		
	elif cms==6:
	#Magento www.lebonmarche.com
		#get_MagentoProductLeBonMarche(bsObj)
		get_MagentoProduct(bsObj)
				

	
