from redfin import Redfin
import requests
import json

client = Redfin()


def get_response(url):
    response = requests.get(
        client.base + url, headers=client.user_agent_header)
    response.raise_for_status()
    return json.loads(response.text[4:])


# Given an address this method will find the exact match in redfin
def find_exact_match(address):
    response = client.search(address)
    url = response['payload']['exactMatch']['url']
    initial_info = client.initial_info(url)

    property_id = initial_info['payload']['propertyId']
    listing_id = initial_info['payload']['listingId']

    mls_data = client.below_the_fold(property_id)
    schools_rating = mls_data['payload']['schoolsAndDistrictsInfo']['servingThisHomeSchools']


# Get all the houses for sale in a given city and home_type
def find_houses_for_sale(city, property_types, **kwargs):
    search_res = client.search(city)
    id = search_res['payload']['exactMatch']['id']
    region_id = id.split('_')[1]
    uipt = []

    for property_type in property_types:
        if property_type == "home":
            uipt.append(str(1))
        elif property_type == "condo":
            uipt.append(str(2))
        elif property_type == "Townhouse":
            uipt.append(str(3))
        elif property_type == "multi-family":
            uipt.append(str(4))
        elif property_type == "land":
            uipt.append(str(5))
        elif property_type == "other":
            uipt.append(str(6))

    if uipt:
        uipt_str = ",".join(uipt)
    else:
        uipt_str = "1,2,3,4,5,6"

    # region_type = 6 (city)
    # uipt - property types (1 = House, 2 = Condo, 3 = Townhouse, 4 = Multi-family, 5 = Land, 6 = Other)
    # sf - listing types (1,7 = Agent-listed homes (includes Redfin listings), 2 = MLS-Listed Foreclosures,
    #                     3 = For sale by owner, 5,6 = New construction)
    # ord - Order
    response = get_response('api/gis?al=1&market=socal&min_stories=1&num_homes=350&ord=redfin-recommended-asc&'
                            'page_number=1&region_id=' + region_id +
                            '&region_type=6&sf=1,2,3,5,6,7&status=9&uipt=' + uipt_str + '&v=8')
    return response['payload']


def filter_results_on_price(payload, price_min_req, price_max_req):
    results = []
    for house in payload:
        price = float(house['price'])
        if price_min_req <= price <= price_max_req:
            results.append(house)
    return results


def filter_results_on_number_of_beds(payload, beds_min_req, beds_max_req):
    results = []
    for house in payload:
        if house['beds'] is not None:
            beds = int(house['beds'])
            if beds_min_req <= beds <= beds_max_req:
                results.append(house)
    return results


def filter_results_on_number_of_baths(payload, no_of_baths):
    results = []
    for house in payload:
        if house['baths'] is not None:
            baths = float(house['baths'])
            if no_of_baths <= baths:
                results.append(house)
    return results


def process_payload(payload):
    output = []
    property_type = "Other"
    for home in payload["homes"]:
        if home["uiPropertyType"] == 1:
            property_type = "Home"
        elif home["uiPropertyType"] == 2:
            property_type = "Condo"
        elif home["uiPropertyType"] == 3:
            property_type = "Townhouse"
        elif home["uiPropertyType"] == 4:
            property_type = "Multi-family"
        elif home["uiPropertyType"] == 5:
            property_type = "Land"

        output.append({
            "mlsId": home["mlsId"]["value"] if "mlsId" in home else None,
            "mlsStatus": home["mlsStatus"] if "mlsStatus" in home else None,
            "price": home["price"]["value"],
            "sqFt": home["sqFt"]["value"] if "value" in home["sqFt"] else None,
            "pricePerSqFt": home["pricePerSqFt"]["value"] if "value" in home["pricePerSqFt"] else None,
            "lotSize": home["lotSize"]["value"] if "value" in home["lotSize"] else None,
            "beds": home["beds"] if "beds" in home else None,
            "baths": home["baths"] if "baths" in home else None,
            "location": home["location"]["value"] if "value" in home["location"] else None,
            "stories": home["stories"] if "stories" in home else None,
            "streetLine": home["streetLine"]["value"],
            "unitNumber": home["unitNumber"]["value"] if "value" in home["unitNumber"] else None,
            "city": home["city"],
            "state": home["state"],
            "zip": home["zip"],
            "postalCode": home["postalCode"]["value"],
            "countryCode": home["countryCode"],
            "status": "Active" if (home["searchStatus"] == 1) else "Not Active",
            "propertyType": property_type,
            "propertyId": home["propertyId"],
            "listingId": home["listingId"],
            "buildingId": home["buildingId"] if "buildingId" in home else None,
            "yearBuilt": home["yearBuilt"]["value"] if "value" in home["yearBuilt"] else None,
            "scanUrl": home["scanUrl"] if "scanUrl" in home else None,
            "posterFrameUrl": home["posterFrameUrl"] if "posterFrameUrl" in home else None,
            "listingAgent": {
                "name": home["listingAgent"]["name"] if "listingAgent" in home else None,
                "redfinAgentId":  home["listingAgent"]["redfinAgentId"] if "listingAgent" in home else None
            },
            "url": "https://www.redfin.com" + home["url"],
            "listingRemarks": home["listingRemarks"] if "listingRemarks" in home else None
        })
    return output


if __name__ == "__main__":
    # address = '4544 Radnor St, Detroit Michigan'
    # find_exact_match(address)
    city = "Boston, MA"
    payload = find_houses_for_sale(city, ["home", "condo"])
    processed_payload = process_payload(payload)
    results = filter_results_on_price(processed_payload, 100000, 450000)
    results = filter_results_on_number_of_beds(results, 1, 2)
    results = filter_results_on_number_of_baths(results, 1)
    print(results)
