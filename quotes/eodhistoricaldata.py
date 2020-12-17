import requests
from project_shared import *

def main():
    debug("__Start main__")
    session = requests.Session()

    url = f'https://eodhistoricaldata.com/api/fundamentals/AAPL.US'
    params = {'api_token': 'OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX'}
    r = session.get(url, params=params)

    if r.status_code == requests.codes.ok:
        debug(r.text)


if __name__ == '__main__':
    print("*********** Start Charter ***********")
    main()
