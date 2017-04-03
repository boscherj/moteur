# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from mot_get_links import *

# ------------------------------------------------------------------------------------------------------------
# CETTE VERSION EST LA GENERIQUE
# ------------------------------------------------------------------------------------------------------------

# la liste des pages		
pages = set()

getLinksInit("bougie-sylvie")

