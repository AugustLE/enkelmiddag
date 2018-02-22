import requests
from bs4 import BeautifulSoup
import json
import ast
import demjson

def crawlRema():

    page = requests.get("https://www.rema.no/butikker/")
    google_api_address = "https://maps.googleapis.com/maps/api/geocode/json?address="
    google_api_key = "AIzaSyBdXrU-e0mk2fYq654325Y0C0Mq76hEbBI"
    soup = BeautifulSoup(page.content, 'html.parser')
    storefinder = soup.find('div', class_="storefinder-treemenu")
    ul_node = list(storefinder.children)[3]

    counties_raw = ul_node.find_all('li', recursive=False)

    response = {"store": "REMA 1000", "counties": []}
    limit = float('inf')
    city_limit = float('inf')
    county_progress = 0

    def get_google_location(address):
        #google_api_request_address = google_api_address + ", " + city_name + ", " + county_name + ", Norway&key=" + google_api_key
        city_position_page = requests.get(address)
        city_position_soup = BeautifulSoup(city_position_page.content, "html.parser")
        city_json_obj = json.loads(str(city_position_soup))
        city_location_obj = list(city_json_obj["results"])[0]["geometry"]["location"]
        lat = city_location_obj["lat"]
        lng = city_location_obj["lng"]

        return lat, lng

    for county in counties_raw:
        if county_progress > limit:
            break
        county_progress += 1
        county_name = county["data-county"]
        county_string = ("Working on " + county_name + ": " + str(county_progress) + "/" + str(len(counties_raw))).encode('utf-8').strip()
        print(county_string)
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
            city_name = city["data-city"]
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
                store_href = store_a["href"]
                #store_id = store_a["data-store-id"]

                try:

                    store_page = requests.get(store_href)
                    store_soup = BeautifulSoup(store_page.content, 'html.parser')
                    scripts = list(store_soup.find("div", class_="page-wrp clearfix wp o-page-wrapper").find_all("script", type="text/javascript"))

                    script_content = list(scripts[1].children)
                    content_piece = script_content[0]

                    new_str = content_piece.replace('storeFinderConfig = ', '')
                    new_obj = new_str.split(',')[3:]

                    obj_str = "{" + new_str.split("$.Deferred()")[1][1:]
                    info_object = demjson.decode(obj_str)["store"]

                    latitude = info_object["latitude"]
                    longitude = info_object["longitude"]
                    name = info_object["name"]
                    phone = info_object["phone"]
                    email = info_object["email"]
                    address = info_object["visitAddress"] + ", "
                    address += info_object["visitPostCode"] + ", "
                    address += "\n" + city_name + ", " + county_name

                    has_post_inStore = info_object["hasPostInStore"]
                    ohObject = info_object["openingHours"]

                    opening_hours = "Mandag: " + ohObject["monday"] + "\n" + \
                    "Tirsdag: " + ohObject["tuesday"] + "\n" + \
                    "Onsdag: " + ohObject["wednesday"] + "\n" + \
                    "Torsdag: " + ohObject["thursday"] + "\n" + \
                    "Fredag: " + ohObject["friday"] + "\n" + \
                    "Lørdag: " + ohObject["saturday"] + "\n"

                    if ohObject["sunday"] == "":
                        opening_hours += "Søndag: stengt"
                    else:
                        opening_hours += "Søndag: " + ohObject["sunday"] + "\n"

                    special_opening_hours = info_object["openingHours"]["specialOpeningHours"]

                    storeObject = {
                        "lat": latitude,
                        "lng": longitude,
                        "name": name.lower().strip(),
                        "phone": phone,
                        "email": email,
                        "address": address,
                        "has_post_in_store": has_post_inStore,
                        "special_opening_hours": special_opening_hours,
                        "opening_hours": opening_hours
                    }
                    cityObject["stores"].append(storeObject)
                except:
                    print("FAIL")
                    continue

            countyObject["cities"].append(cityObject)
        response["counties"].append(countyObject)

    return response
