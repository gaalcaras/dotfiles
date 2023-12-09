#! /bin/env python

from glob import glob
import json
import re
import requests

from pynvim import attach

from utils import notify, get_doi, dl_pdf

DOI = get_doi()

notify(f'Looking up DOI: {DOI}')

RESPONSE = requests.get('http://dx.doi.org/' + DOI,
                        headers={'Accept': 'application/rdf+xml;q=0.5,'
                                           + 'application/vnd.citationstyles.csl+json;q=1.0'})

if RESPONSE.status_code != 200:
    notify(f'Request to dx.doi.org failed with code {RESPONSE.status_code}')

# In nvim, find socket name : "echo v:servername"
NVIM_SOCKETS = glob('/run/user/1000/nvim*')
BUFFERS = []

JSON = json.loads(RESPONSE.text)

def get_field(field):
    if not field in JSON:
        return None

    return JSON[field]

def process_author(field):
    if not field in JSON:
        return None

    return ' and '.join([a['family'] + ', ' + a['given'] for a in JSON['author']])

def get_year(field):
    if not field in JSON:
        return None

    return JSON['issued']['date-parts'][0][0]

def get_number(field):
    if not field in JSON:
        return None

    return JSON['journal-issue']['issue']

def get_pages(number):
    if not 'page' in JSON:
        return None

    pages = JSON['page'].split('-')

    if len(pages) <= number:
        return None

    return pages[number]

FIELDS = {'author':       {'fun': process_author, 'field': 'author'},
          'title':        {'fun': get_field, 'field': 'title'},
          'year':         {'fun': get_year, 'field': 'issued'},
          'journaltitle': {'fun': get_field, 'field': 'container-title'},
          'number':       {'fun': get_number, 'field': 'journal-issue'},
          'doi':          {'fun': get_field, 'field': 'DOI'},
          'p0':           {'fun': get_pages, 'field': 0},
          'p$':           {'fun': get_pages, 'field': 1}
         }

DATA = dict()

def sanitize_string(string):
    if not isinstance(string, str):
        return string

    string = string.strip()
    string = re.sub(r'&', r'\&', string)

    return string

for field, params in FIELDS.items():
    value = params['fun'](params['field'])

    if value is None:
        continue

    DATA[field] = sanitize_string(value)

DONE = False

for socket in NVIM_SOCKETS:
    nvim = attach('socket', path=socket)
    if re.search('master.bib', nvim.command_output('buffers')):
        nvim.vars['bibdata'] = DATA
        nvim.command('call bib#openNewRefBuffer()')
        DONE = True

if not DONE:
    notify('Could not find opened master.bib file.')
