#       Darkorbit Login Example
#       https://github.com/PentoreXannaci

import requests
from bs4 import BeautifulSoup


darkorbit_url = "https://www.darkorbit.com"


def login(username, password):

    login_url = get_login_url()

    #check if the crawler for the login url worked.
    if not login_url:
        print("something went wrong fetching the login url!")
        return

    #post data
    login_data = {"username": username, "password": password}

    #send the login post request with the post data from above.
    login_response = requests.post(login_url, login_data)
    
    #check if the login worked. (search a specific string in the html content which is only present when logged in.)
    if "header_uri" in str(login_response.content):
        print("Logged In.")
    else:
        print("Login Failed.")


def get_login_url():
    #before we can send the login post request. we need to fetch the login url out of the darkorbit site.
    page_response = requests.get(darkorbit_url)

    #init BeautifulSoup with the html response. (pip install beautifulsoup4)
    index_soup = BeautifulSoup(page_response.content, features="html.parser")

    #we are looking for this specific html <form>
    #<form name="bgcdw_login_form" method="post" class="bgcdw_login_form" action="WE ARE LOOKING FOR THIS URL HERE" novalidate="novalidate">
    login_url = index_soup.find("form", {"name":"bgcdw_login_form"})["action"]

    #remove amp; which is sometimes in the url. (no clue why, i actually dont care.)
    login_url = login_url.replace("amp;", "")

    return login_url


username = input("Username: ")
password = input("Password: ")

login(username, password)