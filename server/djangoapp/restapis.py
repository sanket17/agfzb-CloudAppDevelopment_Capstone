import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    # print(kwargs)
    # print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if kwargs.get("api_key"):
            # Basic authentication GET
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        # If any error occurs
        print("Network exception occurred", e)
    return []

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("DEaler",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def post_request(url, json_payload, **kwargs):
    try:
        print("POST to {} with data: {} ".format(url, json_payload))
        res = requests.post(url, params=kwargs, json=json_payload)
        status_code = res.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(res.text)
        return json_data
    except Exception as e:
        # If any error occurs
        print("Network exception occurred", e)
    return {}

def get_dealer_by_id_from_cf(url, dealer_id):
    dealer_doc = get_request(url, id=dealer_id)
    if dealer_doc:
        dealer_doc = dealer_doc[0]
        return CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
    return {}

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    dealer_reviews = get_request(url, id=dealer_id)
    result = []
    if dealer_reviews:
        for dealer_review_doc in dealer_reviews:
            review_obj = DealerReview(
                dealership=dealer_review_doc["dealership"], name=dealer_review_doc["name"], 
                purchase=dealer_review_doc["purchase"], purchase_date=dealer_review_doc.get("purchase_date"), 
                car_make=dealer_review_doc.get("car_make"), car_model=dealer_review_doc.get("car_model"),
                car_year=dealer_review_doc.get("car_year"), id=dealer_review_doc.get("id"), 
                review=dealer_review_doc["review"], sentiment=analyze_review_sentiments(dealer_review_doc["review"]))
            result.append(review_obj)
    return result

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/48123a59-1f30-45da-b644-70c0d7e8c589"
    res = get_request(
        url, 
        api_key="ZexmEUY1WVNtzjXo488cRx-eRwb-V9S_Iq-cZJLITMwl",
        features={
            "sentiment": {}
        },
        text=text,
        version="2019-07-12"
    )
    print('Here-->',res)
    if res:
        return res.get('sentiment', {}).get('document', {}).get('label', '')
    return ''



