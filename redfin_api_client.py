from redfin import Redfin
import requests
import json


class RedfinAPIClient:
    def __init__(self):
        self.client = Redfin()

    def get_response(self, url):
        response = requests.get(
            self.client.base + url, headers=self.client.user_agent_header)
        response.raise_for_status()
        return json.loads(response.text[4:])

    def above_the_folder(self, property_id, **kwargs):
        return self.client.meta_property('aboveTheFold', {'propertyId': property_id, **kwargs}, page=True)

    def list_properties(self, city, property_types, num_beds, min_price, max_price):
        search_res = self.client.search(city)
        id = search_res['payload']['exactMatch']['id']
        region_id = id.split('_')[1]
        uipt = []

        for property_type in property_types:
            if property_type == "home":
                uipt.append(str(1))
            elif property_type == "condo":
                uipt.append(str(2))
            elif property_type == "townhouse":
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
        response = self.get_response('api/gis?al=1&market=socal&min_stories=1&num_homes=10&ord=redfin-recommended-asc&'
                                'min_price=' + str(min_price) + '&max_price=' + str(max_price) +
                                '&num_beds=' + str(num_beds) +
                                '&page_number=1&region_id=' + region_id +
                                '&region_type=6&sf=1,2,3,5,6,7&status=9&uipt=' + uipt_str + '&v=8')
        return response['payload']
