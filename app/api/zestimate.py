# zestimate.py

from requests import get, Session
from bs4 import BeautifulSoup

url = "https://www.zillow.com/homes/{}_rb"

address = "426 S CLARA AVENUE DELAND FL 32720"

def get_zestimate(address):

    address = address.replace(" ", "-")

    zurl = url.format(address)

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}

    session = Session()

    # response = get(zurl, headers=headers)
    response = session.get(zurl)

    print(response.content)
    soup = BeautifulSoup(response.content, "html.parser")

    return soup


if __name__ == "__main__":

    soup = get_zestimate(address)
