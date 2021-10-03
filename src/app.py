#!/usr/bin/env python3
import random
import socket
import sys
import os
import logging

import requests
from prometheus_client import start_http_server, Counter, Gauge, Histogram, Summary
from flask import Flask, request, render_template

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('example-metrics')

BASE_URL = os.environ.get('BASE_URL', '')
PROMETHEUS_PORT = os.environ.get('PROMETHEUS_PORT', 8080)
ENV_LIST = ('qa', 'prod', 'stage',)
HOSTNAME = socket.gethostname()

app = Flask(__name__)
start_http_server(PROMETHEUS_PORT)

request_count = Counter('example_requests_total', 'Count of processed requests', ('method', 'handler',))
bitcoin_gauge = Gauge('example_bitcoin_exchange_rate_dollar', 'Bitcoin to dollar rate')
danger_gauge = Gauge('example_danger', 'Danger gauge', ('env',))
request_latency_histogram = Histogram('example_requests_latency_histogram_seconds', 'Histogram', ('handler',))
request_latency_summary = Summary('example_requests_latency_summary_seconds', 'Summary', ('handler',))

bitcoin_gauge.set_function(lambda: requests.get('https://blockchain.info/ticker').json()['USD']['last'])
for _env in ENV_LIST:
    danger_gauge.labels(env=_env).set(0)


@app.context_processor
def inject_stage_and_region():
    return dict(BASE_URL=BASE_URL)


@app.route('/')
def index():
    request_count.labels(method='get', handler='/').inc()

    val = random.gauss(0.5, 0.2)
    request_latency_histogram.labels(handler='/').observe(val)
    request_latency_summary.labels(handler='/').observe(val)

    return render_template('index.html', hostname=HOSTNAME, envs=ENV_LIST)


@app.route('/latency')
def latency():
    request_count.labels(method='get', handler='/latency').inc()

    val = random.gauss(1.5, 0.6)
    request_latency_histogram.labels(handler='/latency').observe(val)
    request_latency_summary.labels(handler='/latency').observe(val)
    return render_template('page.html', hostname=HOSTNAME, value=val)


@app.route('/danger')
def danger():
    request_count.labels(method='get', handler='/danger').inc()

    val = random.gauss(0.5, 0.2)
    request_latency_histogram.labels(handler='/danger').observe(val)
    request_latency_summary.labels(handler='/danger').observe(val)

    env = request.args.get('env', ENV_LIST[0])
    assert env in ENV_LIST, f'{env} is not in {ENV_LIST}'

    val = int(request.args.get('value', 0))
    assert 0 <= val <= 100, f'danger value {val} must be in range [0, 100]'

    danger_gauge.labels(env=env).set(val)

    return render_template('page.html', hostname=HOSTNAME, value=f'{env} has danger {val}')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
