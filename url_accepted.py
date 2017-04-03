# -*- coding: utf-8 -*-
import re
from urlparse import urlparse

regexesurlautorisee = [ re.compile(p) for p in [ 'rechargeable',
										'pn=2&viewall=off',
										'pn=3&viewall=off',
										'pn=4&viewall=off'
                                     ]
              ]

regexes2 = [ re.compile(p) for p in [ 'mailto',
									#'image',
									 'jpg',
                                     #'#',
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
                                     #'cart',
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
                                     'panier ',
                                     'rss',
                                     'cookies', #28
                                     'catalogsearch',
                                     'sendfriend',
                                     'fidelite',
                                     'legal',
                                     'pdf',
                                     'livraison',
                                     'packaging',
                                     'paiement',	 
                                     'diffuseur',
                                     #'vaporisateur', 
                                     'recharge', #36
                                     #'huile',
                                     'savon',
                                     'gel', #41
                                     'creme', #42
                                     #'decoration',
                                     'sel ',
                                     'bouquet',
                                     'en_us',
                                     'help',
                                     'newsletter',
                                     #'photophore',
                                     'encens',
                                     'lampe',
                                     'bruleur',
                                     #'accessoire',
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
                                     #'p=',
                                     #'store',
                                     'colour=',
                                     'price=',
                                     '__change_site',
                                     'porte-bougie',
                                     #'recherche',
                                     'tablettes',
                                     'cloches',
                                     #'bougeoir',
                                     'coffrets.html?',
                                     'bougies-de-voyage.html?',
                                     'bougies-grand-format.html?',
                                     'bougies-non-parfumees.html?',
                                     #'bougies-parfumees.html?',
                                     'brand=',
                                     'color=', #82
                                     'cat=',
                                     'scent=',
                                     'family=',
                                     'miroir',
                                     'javascript',
                                     'ActionID',
                                     'tri',
                                     'couvercle',
                                     #'parfums-',
                                     'soins-',
                                     'product_compare',
                                     #'galet',
                                     'mode=list',
                                     'theme.html',
                                     'mode=',
                                     'meilleures-ventes',
                                     'lang=en',
                                     'sachets-parfumes',
                                     'bougie-non-parfumee',
                                     #',-verre-', #95
                                     'bougies-led',
                                     'what-s-new',
                                     'photophores.html',
                                     'fragrance-lotion',
                                     'body-mist',
                                     'soap-and-glory',
                                     'conditioner',
                                     'shampoo',
                                     'antibacterien',
                                     'lotion-corporelle',
                                     'brume-parfumee',
                                     'bag-holder',
                                     'abat-jour',
                                     'car-jar',
                                     'language=en',
                                     'brand_id=', #117
                                     'shop_name=', #118
                                     'pommade',
                                     'exterieur',
                                     'occasion',
                                     'parfums-pour-bougies',
                                     'add-to-cart',
                                     'id_lang=1',
                                     'token',
                                     'qty=',
                                     '/en/', #126
                                     'shoe',
                                     'accessor',
                                     #'beauty',
                                     #'sport',
                                     'designerFilter',
                                     'colourFilter',
                                     'keywords',
                                     'filter',
                                     'telecommande',
                                     'eteignoir',
                                     'lumignon',
                                     'briquet',
                                     'allume',
                                     'treestructureguidednavigation',
                                     'brule-parfums',
                                     'non-parfumee',
                                     'dir=asc',
                                     #'%',
                                     '___from_store=',
                                     'votive',
                                     'prefv1',
                                     'outil',
                                     'etouffe-flamme',
                                     'lanterne',
                                     'chaud' #réchaud,
                                     'ciseau',
                                     'coupe-meche',
                                     'chauffe-plat',
                                     'tablette',
                                     'jelly',
                                     'etui',
                                     'flamme-artificielle',
                                     'sort-by',
                                     'chiffre',
                                     #'galet',
                                     'football',
                                     'assiette',
                                     'coupe a',
                                     'pots-pour',
                                     'parfums_theme_yankee'
                                     ]
              ]
    


def url_accepted(Page):                                      

#on verifie que les mots interdits ne sont pas presents dans l url

	#print "Verification : "
	#print Page
	
	accepte_url = 1
	
	for regex3 in regexesurlautorisee:
		if regex3.search(Page):
			#print "URL acceptee : ",Page
			return accepte_url
	
	i = 0		
	for regex2 in regexes2:
		i = i+1
		if regex2.search(Page):
			accepte_url = 0
			print i
			#print "URL refusee"
			return accepte_url
		
	return accepte_url			
	

#pour Amazon
# ---------------------	
def keep_amazon_qid(u, amazon_first_qid):
	parsed_url = urlparse(u)
	
	query=parsed_url.query
	if len(query) > 0:
		x=re.findall("qid=\d*", query)
		if len(x) >0:
			y=x[0]
			z=re.findall("\d*", y)
			if len(z) >4:
				w=z[4]
				v=u.replace(w,amazon_first_qid)
				return(v)

#pour Amazon
# ---------------------	
def get_amazon_first_qid(u):
	parsed_url = urlparse(u)
	
	query=parsed_url.query
	if len(query) > 0:
		x=re.findall("qid=\d*", query)
		if len(x) >0:
			y=x[0]
			z=re.findall("\d*", y)
			if len(z) >4:
				w=z[4]
				print "qid Amazon : "
				print w
				return(w)
				
	return(None)
