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
            raise RequestException
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
    """
    Defines some set colors using escape codes
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

raw_html = simple_get('https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx')
html = BeautifulSoup(raw_html, 'html.parser')

updated = html.find(class_='ms-rteStyle-Quote')
if updated.text is not None:
    print(bcolors.OKBLUE + updated.text + bcolors.ENDC)

rows = html.findAll('tr')
headers = {}
data = []
for row in rows:
    cells = row.findAll("td")
    items = []
    for index in cells:
        items.append(index.text.strip(u'\u200b'))
    data.append(items)
results = list(filter(None, data))

json_out = json.loads(json.dumps(results))
# Remove the stupid table rows that are actually headers
json_out.pop(0)
# Fix the statewide count, we don't care about negative test
json_out[0][0] = 'Statewide'
# Remove the stupid table rows that are actually headers
json_out.pop(1)
# Remove age and hospitalization rate percentages (for now)
for i in range(1, 17):
    json_out.pop(1)

#affected_counties = int(len(json_out)) - 1
print(bcolors.HEADER + "{} cases confirmed statewide".format(json_out[0][1]) + bcolors.ENDC)
print(bcolors.WARNING + bcolors.BOLD + "{} deaths confirmed statewide".format(json_out[0][2]) + bcolors.ENDC)
#print(bcolors.WARNING + bcolors.UNDERLINE + "{} of 67 counties affected".format(affected_counties) + bcolors.ENDC)
for item in json_out:
    county = item[0].strip()
    cases = item[1]
    deaths = item[2].strip('\n') or 0
    if county in ('Lancaster', 'Schuylkill'):
        print(bcolors.WARNING + "Warning: {} active cases in {} county.".format(cases, county) + bcolors.ENDC)
    if county != 'Statewide':
        print("{} county: {} cases, {} deaths".format(county, cases, deaths))
