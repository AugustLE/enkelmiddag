import requests
from bs4 import BeautifulSoup
import json
import ast
import demjson


def crawlKiwi():

    page = requests.get("https://kiwi.no/Finn-butikk/")
    base_url = "https://kiwi.no/"

    google_api_address = "https://maps.googleapis.com/maps/api/geocode/json?address="
    google_api_key = "AIzaSyBdXrU-e0mk2fYq654325Y0C0Mq76hEbBI"

    soup = BeautifulSoup(page.content, 'html.parser')
    storefinder = soup.find('nav', class_="subnav")
    ul_node = storefinder.find("ul", recursive=False)
    counties = list(ul_node.find_all('li', recursive=False))
    response = {"store": "KIWI", "counties": []}

    limit = float('inf')
    city_limit = float('inf')

    def get_google_location(inpput_address):
        position_page = requests.get(inpput_address)
        position_soup = BeautifulSoup(position_page.content, "html.parser")
        json_obj = json.loads(str(position_soup))
        location_obj = list(json_obj["results"])[0]["geometry"]["location"]
        lat = location_obj["lat"]
        lng = location_obj["lng"]

        return lat, lng

    county_progress = 0

    #for i in range(5, len(counties)):
    for county in counties:
        #county = counties[i]
        if county_progress > limit:
            break

        county_progress += 1
        county_name = county.find("a", recursive=False).get_text()
        print(("Working on " + county_name + ": " + str(county_progress) + "/" + str(len(counties))).encode('utf-8').strip())
        google_api_county_address = google_api_address + ", " + county_name + ", Norway&key=" + google_api_key
        county_loc = get_google_location(google_api_county_address)
        county_lat = county_loc[0]
        county_lng = county_loc[1]
        countyObject = {"name": county_name, "lat": county_lat, "lng": county_lng, "cities": []}

        cities = list(county.find("ul", recursive=False).find_all("li", recursive=False))
        city_progress = 0
        for city in cities:
            if city_progress > city_limit:
                break

            city_progress += 1
            city_name = city.find("a", recursive=False).get_text()
            print((city_name + ", " + str(city_progress) + "/" + str(len(cities))).encode('utf-8').strip())
            google_api_request_address = google_api_address + ", " + city_name + ", " + county_name + ", Norway&key=" + google_api_key
            loc_object = get_google_location(google_api_request_address)
            city_lat = loc_object[0]
            city_lng = loc_object[1]

            stores = list(city.find("ul", recursive=False).find_all("li"))

            cityObject = {"name": city_name, "lat": city_lat, "lng": city_lng, "stores": []}
            store_counter = 0
            for store in stores:
                store_counter += 1
                print(str(store_counter) + "/" + str(len(stores)))
                store_a = store.find("a", recursive=False)
                store_name = store.find("span", class_="subnav-storename").get_text()
                store_href = base_url + store_a["href"]

                change_names = ["KIWI  Osan Svolvær", "KIWI  Kvernaland", "KIWI  Cc Mart'n Hamar"];

                change_to_links = ["https://kiwi.no/Finn-butikk/Kiwi-Osan-Svolvar/",
                                 "https://kiwi.no/Finn-butikk/Kiwi-Kvernaland/",
                                 "https://kiwi.no/Finn-butikk/KIWI-CC-Martn-Hamar/"];

                #store_name = store_name.strip()
                if store_name in change_names:

                    store_href = change_to_links[change_names.index(store_name)]

                store_page = requests.get(store_href)
                store_soup = BeautifulSoup(store_page.content, 'html.parser')

                store_info_raw = store_soup.find("div", class_="store-info")
                name = store_soup.find("h1", itemprop="name").get_text()
                opening_hours_node = store_info_raw.find("dl", class_="openinghours")
                opening_hours_list = list(opening_hours_node.children)
                opening_hours_list = list(filter(lambda a: a != "\n", opening_hours_list))

                opening_hours = opening_hours_list[2].get_text() + ": " + opening_hours_list[3].get_text() + ",\n" + \
                                opening_hours_list[4].get_text() + ": " + opening_hours_list[5].get_text()

                if len(opening_hours_list) > 7:
                    opening_hours += ",\n" + opening_hours_list[6].get_text() + ": " + opening_hours_list[7].get_text()

                store_contact_node = store_soup.find("div", class_="store-facts-contact")
                address_node = store_contact_node.find("address")
                store_street_address = address_node.find(itemprop="streetAddress").get_text()
                store_postal_code = address_node.find(itemprop="postalCode").get_text()
                store_postal_place = address_node.find(itemprop="addressLocality").get_text()

                address = store_street_address + ", " +  \
                          store_postal_code + ", " +\
                          store_postal_place + ", " + county_name

                phone = (store_contact_node.find("a", itemprop="telephone").get_text())
                phone = phone.strip(' ')

                geo_node = store_soup.find("div", itemprop="geo")
                latitude = geo_node.find("meta", itemprop="latitude")["content"]
                longitude = geo_node.find("meta", itemprop="longitude")["content"]

                """
                for node in opening_hours_list:
                    cleaned_node = (node.get_text()).strip()
                    print(cleaned_node)
    
                    if cleaned_node == "Hverdager":
                        print(True)
                        opening_hours += cleaned_node + ": " + opening_hours_list[]"""


                storeObject = {
                    "lat": latitude,
                    "lng": longitude,
                    "name": name.lower().strip(),
                    "phone": phone,
                    "email": "",
                    "address": address,
                    "has_post_in_store": "",
                    "special_opening_hours": "",
                    "opening_hours": opening_hours
                }

                cityObject["stores"].append(storeObject)
            countyObject["cities"].append(cityObject)
        response["counties"].append(countyObject)

    return response