# apirl

`apirl` is a Python package designed to manage API rate limits by automatically queuing and pacing API requests. It supports various APIs and provides customizable rate limiting strategies to help avoid hitting API rate limits.

## Installation

You can install `apirl` using pip:

```bash
pip install apirl
```

## Usage

Here is an example of how to use 'apirl' to manage API rate limits:

#### 1. Set Up Environment Variables

Create a .env file in the root directory of your project and add your API keys and any other necessary environment variables:

```
API_KEY=your_api_key_here
```

#### 2. Example Usage

```
import os
from dotenv import load_dotenv
from apirl.core import RateLimiter
from apirl.queue import RateLimitedQueue
import http.client
import ssl
import certifi

# Load environment variables
load_dotenv()

# Initialize RateLimiter and RateLimitedQueue
rate_limiter = RateLimiter(rate_limit=5, per_seconds=10)
rate_limited_queue = RateLimitedQueue(rate_limiter, "https://your-api-base-url.com")

def make_api_call(method, endpoint, headers, body=None):
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        conn = http.client.HTTPSConnection("your-api-host.com", context=context, timeout=10)
        conn.request(method, endpoint, body=body, headers=headers)
        res = conn.getresponse()
        status = res.status
        data = res.read()
        if status == 200:
            print(f"Response for {endpoint}: {data.decode('utf-8')}")
        else:
            print(f"Error {status} for {endpoint}: {data.decode('utf-8')}")
    except (http.client.HTTPException, ssl.SSLError) as e:
        print(f"Network error for {endpoint}: {e}")

if __name__ == "__main__":
    headers = {
        'Authorization': f'Bearer {os.getenv("API_KEY")}',
        'Content-Type': 'application/json'
    }
    endpoints = [
        ('GET', '/endpoint', headers)
    ]
    for method, endpoint, headers in endpoints:
        rate_limited_queue.put(make_api_call, method, endpoint, headers)
    rate_limited_queue.queue.join()
```
## Features

- Rate Limiter: Manages and enforces API rate limits with configurable limits and intervals.
- Rate-Limited Queue: Queues API requests and ensures they are sent within rate limit constraints.
- Customizable Headers: Supports custom headers for API requests.
- SSL Certificate Handling: Uses certifi to manage SSL certificates.

## Contributing 

Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests through GitHub issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.