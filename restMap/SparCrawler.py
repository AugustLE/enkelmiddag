import requests
from bs4 import BeautifulSoup
import json
import ast
import demjson


def crawlSpar():

    page = requests.get("https://spar.no/Finn-butikk/")
    base_url = "https://spar.no"

    google_api_address = "https://maps.googleapis.com/maps/api/geocode/json?address="
    google_api_key = "AIzaSyBdXrU-e0mk2fYq654325Y0C0Mq76hEbBI"

    soup = BeautifulSoup(page.content, 'html.parser')
    storefinder = soup.find('nav', class_="col-menu storelist-menu")

    ul_node = storefinder.find("div", id="js_subnav").find("ul", recursive=False)
    counties_list = list(ul_node.find_all('li', recursive=False))
    response = {"store": "Spar", "counties": []}

    def get_google_location(inpput_address):
        position_page = requests.get(inpput_address)
        position_soup = BeautifulSoup(position_page.content, "html.parser")
        json_obj = json.loads(str(position_soup))
        location_obj = list(json_obj["results"])[0]["geometry"]["location"]
        lat = location_obj["lat"]
        lng = location_obj["lng"]
        return lat, lng

    limit = float('inf')
    city_limit = float('inf')
    county_progress = 0

    for county in counties_list:
        if county_progress > limit:
            break

        county_progress += 1
        county_name = county.find("a", recursive=False).get_text()
        print(county_name)
        print("Working on " + county_name + ": " + str(county_progress) + "/" + str(len(counties_list)))
        google_api_county_address = google_api_address + ", " + county_name + ", Norway&key=" + google_api_key
        county_loc = get_google_location(google_api_county_address)
        county_lat = county_loc[0]
        county_lng = county_loc[1]

        countyObject = {"name": county_name, "lat": county_lat, "lng": county_lng, "stores": []}

        stores = list(county.find("ul", recursive=False).find_all("li", recursive=False))

        city_progress = 0

        for store in stores:
            city_progress += 1

            store_a = store.find("a", recursive=False)
            store_href = base_url + store_a["href"]

            change_links = ["/Finn-butikk/SPAR-Amfi-Forde"];
            changeToLinks = ["/Finn-butikk/SPAR-Handelshuset-Forde"];

            if store_href in change_links:
                store_href = changeToLinks[change_links.index(store_href)]

            store_page = requests.get(store_href)
            store_soup = BeautifulSoup(store_page.content, 'html.parser')
            try:
                opening_hours_node = store_soup.find("dl", class_="openinghours")
                opening_hours_list = list(opening_hours_node.children)
                opening_hours_list = list(filter(lambda a: a != "\n", opening_hours_list))
                opening_hours = opening_hours_list[0].get_text() + ": " + opening_hours_list[1].get_text() + ",\n" + \
                                opening_hours_list[2].get_text() + ": " + opening_hours_list[3].get_text() + ",\n" + \
                                opening_hours_list[4].get_text() + ": " + opening_hours_list[5].get_text()

                info_node = store_soup.find("div", class_="store-facts")
                contact_info_node = info_node.find("div", class_="contact")

                store_street_address = contact_info_node.find(itemprop="streetAddress").get_text()
                store_postal_code = contact_info_node.find(itemprop="postalCode").get_text()
                store_postal_place = contact_info_node.find(itemprop="addressLocality").get_text()

                address = store_street_address + ", " + \
                          store_postal_code + ", " + \
                          store_postal_place + ", " + county_name

                email_node = info_node.find("a", itemprop="email")
                email = email_node["href"].replace("mailto:", "")

                geo_node = store_soup.find("div", itemprop="geo")
                latitude = geo_node.find("meta", itemprop="latitude")["content"]
                longitude = geo_node.find("meta", itemprop="longitude")["content"]

                name = store_soup.find("h1", itemprop="name").get_text()
                name = name.strip()
                print(name + ", " + str(city_progress) + "/" + str(len(stores)))

                storeObject = {
                    "lat": latitude,
                    "lng": longitude,
                    "name": name.lower(),
                    "phone": "",
                    "email": email,
                    "address": address,
                    "has_post_in_store": "",
                    "special_opening_hours": "",
                    "opening_hours": opening_hours
                }

                countyObject["stores"].append(storeObject)
            except:
                print("FAIL FAIL")
                continue
        response["counties"].append(countyObject)

    return response