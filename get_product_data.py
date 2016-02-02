# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *from get_product_data_magento import *
from get_product_data_prestashop import *
from get_product_data_joomla import *
from get_product_data_W import *
#Pour rappel : #Magento 1
#PrestaShop 2
#WooCommerce 3
#4Joomla 4

	
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
				

	
