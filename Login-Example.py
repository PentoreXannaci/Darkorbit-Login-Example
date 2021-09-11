#       Darkorbit Login Example
#       https://github.com/PentoreXannaci

import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup

darkorbit_client_updates_url = "https://darkorbit-22-client.bpsecure.com/bpflashclient/windows.x64/repository/Updates.xml"
darkorbit_url = "https://www.darkorbit.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br"
    }


def login(username, password):

    login_url = get_login_url()

    #check if the crawler for the login url worked.
    if not login_url:
        print("something went wrong fetching the login url!")
        return

    #post data
    login_data = {"username": username, "password": password}

    #send the login post request with the post data from above.
    login_response = requests.post(login_url, login_data, headers = headers)
    
    #check if the login worked. (search a specific string in the html content which is only present when logged in.)
    if "header_uri" in str(login_response.content):
        print("Logged In.")
    else:
        print("Login Failed.")


def get_login_url():
    #before we can send the login post request. we need to fetch the login url out of the darkorbit site.
    page_response = requests.get(darkorbit_url, headers = headers)

    #init BeautifulSoup with the html response. (pip install beautifulsoup4)
    index_soup = BeautifulSoup(page_response.content, features="html.parser")

    #we are looking for this specific html <form>
    #<form name="bgcdw_login_form" method="post" class="bgcdw_login_form" action="WE ARE LOOKING FOR THIS URL HERE" novalidate="novalidate">
    login_url = index_soup.find("form", {"name":"bgcdw_login_form"})["action"]

    #remove amp; which is sometimes in the url. (no clue why, i actually dont care.)
    login_url = login_url.replace("amp;", "")

    return login_url

def set_useragent():
    updates_response = requests.get(darkorbit_client_updates_url, headers = headers)
    tree = ET.fromstring(updates_response.content)

    package_update_version = tree.find(".//Version").text
    headers["User-Agent"] = f"BigPointClient/{package_update_version}"


#set the useragent to the darkorbit client useragent. 
set_useragent()
username = input("Username: ")
password = input("Password: ")

login(username, password)