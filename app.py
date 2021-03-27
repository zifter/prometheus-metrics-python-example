#!/usr/bin/env python3
import random
import sys
import os
import logging
from random import randint

import requests
from prometheus_client import start_http_server, Counter, Gauge, Histogram, Summary
from flask import Flask

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('metrics-example')

app = Flask(__name__)
start_http_server(os.environ.get('PROMETHEUS_PORT', 8080))

request_count = Counter('requests_total', 'Count of requests was processed by application', ('method', 'endpoint',))
bitcoin_gauge = Gauge('bitcoin_exchange_rate_dollar', 'Bitcoin to dollar rate')
request_latency_histogram = Histogram('request_latency_histogram_seconds', 'Description of histogram')
request_latency_summary = Summary('request_latency_summary_seconds', 'Description of histogram')

bitcoin_gauge.set_function(lambda: requests.get('https://blockchain.info/ticker').json()['USD']['last'])


@app.route('/')
def index():
    request_count.labels(method='get', endpoint='/').inc()
    return 'Index Page'


@app.route('/latency')
def latency():
    request_count.labels(method='get', endpoint='/latency').inc()

    v = random.gauss(1.0, 0.6)
    request_latency_histogram.observe(v)
    request_latency_summary.observe(v)
    return str(v)
