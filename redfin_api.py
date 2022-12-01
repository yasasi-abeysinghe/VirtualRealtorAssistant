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


# Get all the houses for sale in a given city
def find_houses_for_sale(city, **kwargs):
    search_res = client.search(city)
    id = search_res['payload']['exactMatch']['id']
    region_id = id.split('_')[1]

    # region_type = 6 (city)
    # uipt - property types (1 = House, 2 = Condo, 3 = Townhouse, 4 = Multi-family, 5 = Land, 6 = Other)
    # sf - listing types (1,7 = Agent-listed homes (includes Redfin listings), 2 = MLS-Listed Foreclosures,
    #                     3 = For sale by owner, 5,6 = New construction)
    # ord - Order
    response = get_response('api/gis?al=1&market=socal&min_stories=1&num_homes=350&ord=redfin-recommended-asc&'
                            'page_number=1&region_id=' + region_id +
                            '&region_type=6&sf=1,2,3,5,6,7&status=9&uipt=1,2,3,4,5,6,7,8&v=8')
    for house in response['payload']['homes']:
        print(house)


if __name__ == "__main__":
    address = '4544 Radnor St, Detroit Michigan'
    find_exact_match(address)
    city = "Boston, MA"
    find_houses_for_sale(city)

