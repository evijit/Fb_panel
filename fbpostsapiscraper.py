import requests
import brotli
import json
import re
from urllib.parse import unquote
import time
from bs4 import BeautifulSoup
import traceback
import html.parser
import os, datetime
import random
import urllib.request
import base64

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def retry_session(retries, session=None, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

sess = retry_session(retries=5)


token = 'RUFBQnNiQ1MxaUhnQkFDOFgyZnd4OUJuWDZBTDBoRDhCUUxNVHI4dGV0bXBiQkZlMDNUVlcxdXczSlMzY0paQ2JyZG5HdWxBbmtXNDhBamt3VExQbWZFRGZvd0lseGZyb1NOQ0tueVpDSWFIM1A0Tmk3VElRWXpZZWRDZ1pCdG5UNWlsUmdiMWtQZ3pMN0taQlpCVE5wUWdrVmpMa0hKTHRJTWZRYmpoT1Ayd1pEWkQ='



def getposts(pid,lim):

    url = "https://graph.facebook.com/v3.2/"+pid+"/posts?fields=from%2Cmessage%2Cto%2Clikes%2Ccoordinates%2Cdescription%2Clink%2Ccreated_time%2Cfull_picture&limit="+str(lim)+"&access_token="+ base64.b64decode(token).decode('utf-8')

    print(url)

    try:
        contents = urllib.request.urlopen(url).read()
        ob = json.loads(contents)
        return ob

    except:
        traceback.print_exc()
        return None


