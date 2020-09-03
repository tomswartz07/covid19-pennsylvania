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

raw_html = simple_get('https://www.health.pa.gov/topics/disease/coronavirus/Pages/Coronavirus.aspx')
html = BeautifulSoup(raw_html, 'html.parser')

updated = html.find(class_='ms-rteForeColor-2')
if updated.text == '':
    updated_text = "Unable to get updated time"
    print(bcolors.OKBLUE + updated_text + bcolors.ENDC)
elif updated.text is not None:
    updated_text = updated.text.replace('\n', '').replace('  ', '')
    print(bcolors.OKBLUE + updated_text + bcolors.ENDC)

rows = html.findAll('tr')
headers = {}
data = []
for row in rows:
    cells = row.findAll("td")
    items = []
    for index in cells:
        item = index.text.rstrip('\u200b')
        item = item.strip('\n*\r')
        item.replace("*", "")
        item.replace("\n", "")
        item.replace("\u200b", "")
        items.append(item)
    data.append(items)
results = list(filter(None, data))

json_out = json.loads(json.dumps(results))
# Remove the stupid table rows that are actually headers
#json_out.pop(0)
# Fix the statewide count, they're including probable cases in the count now
json_out[0].insert(0, 'Statewide')
# Remove the stupid table rows that are actually headers
#json_out.pop(1)
# Handle the full statewide info
#json_out[1].insert(0, 'Statewide')
# Remove age and hospitalization rate percentages- not accurate
# They're also showing an estimated (lol) percentage of recovered.
# Three asterisks proceed this recovered number, so we'll just ignore it too.
#for i in range(1, 18):
#    json_out.pop(1)

#affected_counties = int(len(json_out)) - 1

# Apparently they're publishing Nursing Home data too?
# Kind of niche for the topic page
# Regardless, get rid of it from our output
#
# Heading gets cleared here, county homes get
# skipped below
#json_out.pop(68)

# Cool, also jamming demographic info in with no proper headers
# Would be great if they didn't randomly update the page
# and stuff various tables all over the place with no unique ids.
# Let's drop that info off because it's not really relevant for this
#del json_out[68:]

# OF COURSE the order for unconfirmed, confirmed, and deaths are different than
# the per-county table
print(bcolors.HEADER + "{} total cases statewide".format(json_out[0][1].strip('*').strip('\n')) + bcolors.ENDC)
#print(bcolors.HEADER + "…of which {} are probable/unconfirmed cases".format(json_out[1][2]) + bcolors.ENDC)
#print(bcolors.WARNING + bcolors.BOLD + \
#        "{} total deaths statewide".format(json_out[0][2]) + bcolors.ENDC)
#print(bcolors.WARNING + bcolors.BOLD + \
#        "…of which {} are probable/unconfirmed deaths".format(json_out[1][4]) + bcolors.ENDC)
#for item in json_out:
#    print(item)
#    county = item[0].strip()
#    cases = item[3].replace('*', '')
#    negatives = item[2].replace('*', '')
#    deaths = "N/A"  #item[3].strip('\n') or 0
#    if len(item) == 3:
#        if county in ('Lancaster', 'Schuylkill'):
#            print(bcolors.WARNING + "Warning: {} cases, {} deaths in {} county.".format(cases, deaths, county) + bcolors.ENDC)
#        if county not in ('Statewide', 'Probable'):
#            print("{} county: {} cases, {} deaths".format(county, cases, deaths))
#    elif len(item) > 3:
#        pass
