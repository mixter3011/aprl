# example_usage.py

import os
import json
from dotenv import load_dotenv
from aprl.core import RateLimiter
from aprl.queue import RateLimitedQueue
import http.client
import ssl
import certifi
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def make_api_call(method, endpoint, headers, body=None):
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        conn = http.client.HTTPSConnection("linkedin-data-api.p.rapidapi.com", context=context, timeout=10)
        conn.request(method, endpoint, body=body, headers=headers)
        res = conn.getresponse()
        status = res.status
        data = res.read()

        if status == 200:
            try:
                parsed_data = json.loads(data.decode('utf-8'))
                logging.info(f"Response for {endpoint}: {json.dumps(parsed_data, indent=2)}")
            except json.JSONDecodeError:
                logging.info(f"Response for {endpoint}: {data.decode('utf-8')}")
        else:
            logging.error(f"Error {status} for {endpoint}: {data.decode('utf-8')}")

    except (http.client.HTTPException, ssl.SSLError) as e:
        logging.error(f"Network error for {endpoint}: {e}")

if __name__ == "__main__":
    rate_limiter = RateLimiter(rate_limit=5, per_seconds=10)
    rate_limited_queue = RateLimitedQueue(rate_limiter, "https://linkedin-data-api.p.rapidapi.com")

    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    if not rapidapi_key:
        logging.error("API key not found in environment variables")
        exit(1)

    headers = {
        'x-rapidapi-key': rapidapi_key,
        'x-rapidapi-host': "linkedin-data-api.p.rapidapi.com"
    }

    endpoints = [
        ('GET', '/?username=username', headers),
        ('POST', '/some-endpoint', headers, '{"key": "value"}'),
        # Add more endpoints as needed
    ]

    logging.info("Starting to queue API requests")

    for method, endpoint, headers, *body in endpoints:
        rate_limited_queue.put(make_api_call, method, endpoint, headers, *body)

    rate_limited_queue.queue.join()
    logging.info("All API requests completed")
