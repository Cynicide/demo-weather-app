
import logging, sys, json, os
from libs import weather as wt
from flask import Flask, request, make_response, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Set up basic prometheus metrics as Cloud Watch can scrape
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

# Grab the API Key from the Env Vars 
apikey = os.environ['OPENWEATHER_APIKEY']
app_apikeys = wt.import_apikeys()

# Default Route
@app.route('/')
def root_response():
    return 'Basic Usage: '

# Weather App Route
@app.route('/api', methods=["POST"])
def get_weather():
    
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    app.logger.info("Incoming API POST: for " + ip_addr)
    
    if (request.headers.get('apikey') not in app_apikeys):
        app.logger.error("Error: Invalid API Key from: " + ip_addr)
        return(make_response("Unauthorized", 400))

    # Attempt to Fetch the Weather Data
    response = wt.clean_request(request.args, apikey)
    
    # Turn any textual responses into json
    data = json.loads(response['text'])

    # Create a flask response, set the status code and send
    return(make_response(data, response['status_code']))
