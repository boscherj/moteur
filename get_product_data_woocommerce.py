# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from enregistrement import *

#ATTENTION DEUX FOIS LE MEME NOM POUR UNE FONCTION A CORRIGER
#----------------------------------------------------------------------------------------------
#fonction qui verifie que la page produit Woocommerce est celle d une bougie	
def ex_give_WoocommerceWordpressProductName(bsObj):
	
	check = False
	print "check_est_une_bougie_Woocommerce"
		
	#Cas Scandles		
	nom = bsObj.find("h1", {"itemprop":"name"})
	if nom != None:
		nom_produit = nom.get_text()
		print "1er cas"
		print nom_produit
		if est_ce_une_bougie(nom_produit):
			check = True
			return check	
					
	return check

#---------------------------------------------------------------------------------
#on cherche le nom du produit 
def give_WoocommerceWordpressProductName(bsObj, produit):

	produit_title = bsObj.find("h1", {"itemprop":"name"})
	if produit_title != None:
		nom_produit = produit_title.get_text()
		#print nom_produit
		#if  check_est_une_bougie_WordpressProductName(bsObj):
		return nom_produit
			
	return ""

#---------------------------------------------------------------------------------
#on vérifie que c'est bien un produit Wordpress Woocommerce 
def check_WoocommerceWordpressIsItAproduct(bsObj):

	#Il y a plusieurs possibilites pour que ce soit une page produit
	#Soit il y a un prix dans meta itemprop
	#Soit il y a un prix dans p itemprop
	produit=bsObj.find("meta", {"itemprop":"price"})
	if produit!= None: 
		return produit
		
	#cas 2	
	produit= bsObj.find("p", {"itemprop":"price"})
	if produit!= None: 
		return produit

	#ce n'est pas un produit
	return produit	


#---------------------------------------------------------------------------------
#cherche le prix d'un produit Prestashop
def check_WoocommerceWordpressProductPriceSolde(bsObj):

	old_prix = None
	
	allprix = bsObj.find("div", {"itemprop":"offers"})
	if allprix != None:
		prix1=allprix.find("span", {"class":"amount"})
		if prix1 != None:
			old_prix=prix1.find_next("span", {"class":"amount"})
			if old_prix != None:
				return old_prix
	
	return old_prix
		
#---------------------------------------------------------------------------------
#cherche le prix d'un produit Woocommerce Wordpress
def check_WoocommerceWordpressProductPrice(bsObj):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	

	#1er cas
	prix = bsObj.find("meta", {"itemprop":"price"})
	if prix != None:
		prixTxt = prix['content']
	
	else:
		prix = bsObj.find("p", {"itemprop":"price"})
		if prix != None:	
			prixTxt = prix.get_text()


	#prix soldé	
	old_prix = check_WoocommerceWordpressProductPriceSolde(bsObj)
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
def get_WoocommerceWordpressProduct(bsObj):

	produit = check_WoocommerceWordpressIsItAproduct(bsObj)			
	if produit != None: 
	
		#on teste si c'est une bougie
		nom_produit = give_WoocommerceWordpressProductName(bsObj, produit)
		if nom_produit != "":
			produit_actif.add_NomProduit(nom_produit)
			
			print nom_produit	
			print "On cherche le prix"	
			
			prix, old_price, special_price = check_WoocommerceWordpressProductPrice(bsObj)
			
			if prix != None: 
				print prix
				produit_actif.add_PrixProduit(prix, old_price, special_price)
				imgUrlSrc = give_WoocommerceWordpressProductImgURL(bsObj)
				if imgUrlSrc != "":
					#print imgUrlSrc
					produit_actif.add_UrlImageProduit(imgUrlSrc)

