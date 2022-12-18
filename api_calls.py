from redfin_api_client import RedfinAPIClient

redfin_client = RedfinAPIClient()


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

        photos = redfin_client.above_the_folder(home["propertyId"])["payload"]["mediaBrowserInfo"]["photos"]
        photo_urls = []
        for photo in photos:
            photo_urls.append(photo["photoUrls"]["fullScreenPhotoUrl"])

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
            "listingRemarks": home["listingRemarks"] if "listingRemarks" in home else None,
            "photoUrls": photo_urls[0] if photo_urls != [] else None
        })

    return output


def get_results(city, property_types, num_beds, min_price, max_price):
    payload = redfin_client.list_properties(city, property_types, num_beds, min_price, max_price)
    results = process_payload(payload)
    if not results:
        return "No results for that search"
    return results
