import json
from contextlib import closing
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            print("Unable to get page...")
            return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

raw_html = simple_get('https://www.health.pa.gov/topics/disease/Pages/Coronavirus.aspx')
html = BeautifulSoup(raw_html, 'html.parser')

updated = html.find('em')
if updated.text is not None:
    print(bcolors.OKBLUE + updated.text + bcolors.ENDC)

tds = [row.findAll('td') for row in html.findAll('tr')]
results = {td[0].string: td[1].string for td in tds}
del results['\u200bNegative']
results['Statewide'] = results.pop('1,187')

json_out = json.loads(json.dumps(results))
print(bcolors.HEADER + "{} cases confirmed statewide".format(json_out['Statewide']) + bcolors.ENDC)
for county, cases in json_out.items():
    if county != 'Statewide':
        print("{:>4}: {}".format(cases, county))
    if county == 'Lancaster' or county == 'Schuylkill':
        print(bcolors.WARNING + "Warning: {} active cases in {} county.".format(cases, county) + bcolors.ENDC)
