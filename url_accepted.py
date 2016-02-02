# -*- coding: utf-8 -*-
import re
from urlparse import urlparse


regexes2 = [ re.compile(p) for p in [ 'mailto',
									'image',
									 'jpg',
                                     '#',
                                     'png',
                                     'cadeau',
                                     'recrutement',
                                     'engagement',
                                     "revendeur",
                                     "product_id",
                                     "alert",
                                     'wp-content',
                                     'uploads',
                                     'checkout',
                                     'cart',
                                     'account',
                                     'wishlist',
                                     'sitemap',
                                     'robot',
                                     'zip',
                                     'contact',
                                     'compte',
                                     'commande',
                                     'order',
                                     'cms',
                                     'history',
                                     'panier',
                                     'rss',
                                     'cookies',
                                     'catalogsearch',
                                     'sendfriend',
                                     'fidelite',
                                     'legal',
                                     'pdf',
                                     'livraison',
                                     'packaging',
                                     'paiement',	 
                                     'diffuseur',
                                     'vaporisateur',
                                     'recharge',
                                     'huile',
                                     'savon',
                                     'gel',
                                     'creme',
                                     'decoration',
                                     'sel',
                                     'bouquet',
                                     'en_us',
                                     'help',
                                     'newsletter',
                                     'photophore',
                                     'encens',
                                     'lampe',
                                     'bruleur',
                                     'accessoire',
                                     'concentr',
                                     'passe',
                                     'adresse',
                                     'connexion',
                                     'store=en',
                                     'aide',
                                     'pochette',
                                     'recharge',
                                     'from_store=fr_fr',
                                     'currency',
                                     'blog'	,
                                     'google',
                                     'twitter',
                                     'facebook',
                                     'share',
                                     'lingerie',
                                     'pinterest',
                                     'p=',
                                     'store',
                                     'colour=',
                                     'price='
                                     ]
              ]
    


def url_accepted(Page):                                      

#on verifie que les mots interdits ne sont pas presents dans l url

	accepte_url = 1
	
	for regex2 in regexes2:
		if regex2.search(Page):
			accepte_url = 0
			return accepte_url
		
	return accepte_url			
