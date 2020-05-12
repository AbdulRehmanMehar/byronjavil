# zestimate.py

from requests import get, Session
from bs4 import BeautifulSoup

ZWSID = "X1-ZWz179bo49g7wr_8mfo0"

url = "http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={ZWSID}&address={ADDRESS}&citystatezip={STATEZIP}"

address = "426 S CLARA AVENUE DELAND FL 32720"

def get_zestimate(address):

    

    city_zip = "+".join(address.split(" ")[-2:])
    address = "+".join(address.split(" ")[:-2])

    zurl = url.format(ZWSID=ZWSID, ADDRESS=address, STATEZIP=city_zip)

    print(zurl)
    
    response = get(zurl)

    print(response.content)
    soup = BeautifulSoup(response.content, "html.parser")

    return soup


if __name__ == "__main__":

    soup = get_zestimate(address)
