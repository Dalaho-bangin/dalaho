import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from core.importer import importer
import requests




def requester(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        response = requests.get(url,
            headers=headers,
            verify=False,
            allow_redirects=False,
            timeout=5
            )
        return response
    except Exception as e:
        return str(e)


def create_query(params):
    """
    creates a query string from a list of parameters
    returns str
    """
    query_string = ''
    for param in params:
        pair = param + '=' + 'dalaho' + '&'
        query_string += pair
    if query_string.endswith('&'):
        query_string = query_string[:-1]
    return  query_string



def update_request(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    for q in query_params:
        query_params[q]=['dalaho']

    encoded_query = urlencode(query_params, doseq=True)
    new_url = urlunparse((
    parsed_url.scheme,
    parsed_url.netloc,
    parsed_url.path,
    parsed_url.params,
    encoded_query,
    parsed_url.fragment
    ))
    return new_url

    


def extract_js(response):
    """
    extracts javascript from a given string
    """
    scripts = []
    for part in re.split('(?i)<script[> ]', response):
        actual_parts = re.split('(?i)</script>', part, maxsplit=2)
        if len(actual_parts) > 1:
            scripts.append(actual_parts[0])
    return scripts


def prepare_requests(args):
   
 
    if args.import_file:
        return importer(args.import_file)
    return []

