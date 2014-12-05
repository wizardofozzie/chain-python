from chain import SDKVersion
import requests

def request(URI, data=""):
    headers = {
        'User-Agent': "chain-python " + SDKVersion,
        'Accept-Encoding': 'GZIP',
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }
    r = requests.get(URI, data=data, headers=headers, timeout=10, verify=True, allow_redirects=False)
    return r.text


    