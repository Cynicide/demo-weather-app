import requests as r
import logging, sys, json, os

logging.basicConfig(stream = sys.stdout, level = logging.INFO)

def import_apikeys():
    raw_apikeys = os.environ['APIKEYS']
    apikeys=raw_apikeys.split(",")
    return(apikeys)

def locate_city(request_args, apikey):
    
    city = request_args['City']
    country = request_args['Country']

    logging.info("Attemping to locate " + city + " in " + country)
    
    # I would prefer to have a higher limit here but I ran into issues where openweather would return
    # multiple instances of the same city and slightly different coordinates. Accomdating this was a lower priority 
    url = "http://api.openweathermap.org/geo/1.0/direct?q="+ str(city) + "," + str(country) +"&limit=1&appid=" + str(apikey)
    
    # Try to get the City Latitude and Longitude
    try:
        response = (r.get(url))
    except:
        logging.exception("Error: Exception locating city")
        pass
    
    if (response.status_code != 200):
        resp = {}
        resp['status_code'] = response.status_code
        resp['text'] = response.text
        return(resp)

    location = json.loads(response.text)
    
    # If the location data is empty we didn't match a city/country
    if (len(location) == 0):
        resp = {}
        resp['status_code'] = 400
        resp['text'] = '{"message": "City Name: ' + str(city) + ' and Country Name ' + str(country) +' could not be located."}'
        return(resp)

    # If we got a match return it with the logitude and latitude
    resp = {}

    resp['status_code'] = response.status_code
    resp['text'] = response.text
    resp['lon'] = location[0]['lon']
    resp['lat'] = location[0]['lat']
    resp['city'] = city
    resp['country'] = country 
    
    return(resp)

def clean_request(request_args, apikey):
    logging.info("Cleaning Request.")
    
    response = {}

    # Test to see if the two parameters are not present or empty or blank
    if ('Country' not in request_args or 'City' not in request_args):
        response['status_code'] = 400
        response['text'] = '{"message" : "Bad Request: Please Include Country and City Parameters"}'
        logging.info(response)
        return(response)        
    
    if (request_args['Country'] == "" or request_args['City'] == ""):
        response['status_code'] = 400
        response['text'] = '{ "message": "Bad Request: Country or City Cannot be Blank"}'
        return(response)

    if (request_args['Country'] is None or request_args['City'] is None):
        response['status_code'] = 400
        response['text'] = '{ "message": "Bad Request: Country or City Cannot be Blank"}'
        return(response)

    logging.info("Calling OpenWeather Location API")
    
    # Call the OpenWeather Geo API to locate the city
    location = locate_city(request_args, apikey)
    
    # If we could not find the City and Country at Openweather then return the response to the user
    if (location['status_code'] == 400):
        return(location)
    
    # Use the location to get the weather
    weather = get_weather(location, apikey)
    return(weather)

def get_weather(location, apikey):
    lat = location['lat']
    lon = location['lon']

    logging.info("Fetching Weather for " + location['city'] + " in " + location['country'])
    
    url = "https://api.openweathermap.org/data/2.5/weather?lat="+ str(lat) + "&lon=" + str(lon) +"&appid=" + str(apikey)
    
    try:
        response = (r.get(url))
    except:
        logging.exception("Error: Exception thrown reading error.")

    if (response.status_code != 200):
        resp = {}
        resp['status_code'] = response.status_code
        resp['text'] = response.text
        return(resp)

    resp = {}
    resp['status_code'] = response.status_code
    resp['text'] = response.text
    return(resp)