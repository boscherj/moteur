# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from enregistrement import *

#---------------------------------------------------------------------------------

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
def get_PrestaShopProduct(bsObj):
	print "PrestaShop"
	
	#plusieurs possibilites pour savoir si la page est un produit
	isPageProduit1=bsObj.find("body", {"id":"product"})
	isPageProduit2= bsObj.find("div", {"class":"product_attributes"})
	if isPageProduit1!= None: 
		print "produit"
		isPageProduit = isPageProduit1
	else:
		if isPageProduit2!= None: 	
			print "produit"
			isPageProduit = isPageProduit2
		else:
			print "Pas un produit"
			isPageProduit = None		
			
	#page produit
	if isPageProduit != None: 
	
		if check_est_une_bougie_PrestaShop(bsObj):
			produit = bsObj.find("title")
			nom_produit = produit.get_text()
			print nom_produit	
			print "On cherche le prix"	
			#span
			#1er cas
			prix = bsObj.find("span", {"class":"our_price_display"})
			if prix == None:
				#2eme cas
				prix = bsObj.find("p", {"class":"our_price_display"})
				if prix != None:	
					prix_produit = prix.get_text()
					print prix_produit
				else:
					print "Pas de prix"
			else:
				prix_produit = prix.get_text()
				print prix_produit			
		#pas une bougie
		else:
			print "Pas une bougie"
