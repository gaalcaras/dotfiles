#! /bin/env python

import os
import re
import shlex
import subprocess
import sys

from datetime import date

import requests
import mechanicalsoup

def get_nvim_servers():
    output = subprocess.run(['nvr', '--serverlist'], check=True, capture_output=True, text=True)
    servers = output.stdout.split('\n')
    return servers

def notify(message = ''):
    """
    Send desktop notification
    """
    msg = f'notify-send -u low -a "getdoi.py" "{message}"'
    subprocess.run(shlex.split(msg), check=True)

def get_doi():
    """
    Get DOI from QUTEBROWSER webpage
    """
    DOI_R = re.compile(r'10.\d{4,9}/[-._;()/:\w]+')
    DOIS = []

    with open(os.path.expandvars('$QUTE_TEXT'), 'r', encoding='utf8') as page_f:
        for _, line in enumerate(page_f):
            if re.search(DOI_R, line):
                DOIS.append(line)

    if len(DOIS) > 1:
        COMMAND = 'rofi -dmenu -i -theme dark'
        ENV = os.environ.copy()
        ENV['ROFIACCENT'] = '#b5bd68'

        PROCESS = subprocess.run(shlex.split(COMMAND),
                                 input=''.join(DOIS).encode('UTF-8'), env=ENV,
                                 check=True, stdout=subprocess.PIPE)

        OUTPUT = PROCESS.stdout.decode('UTF-8').strip()
    else:
        if not DOIS:
            notify('No DOI was found')
            sys.exit()

        OUTPUT = DOIS[0]

    MATCH = re.search(DOI_R, OUTPUT)
    if MATCH:
        DOI = MATCH.group(0)
    else:
        notify('No valid DOI :(')
        sys.exit()

    return DOI

def get_scihub_urls():
    """
    Get a valid SciHub URL
    """

    br = mechanicalsoup.StatefulBrowser()
    br.open('https://sci-hub.tech', verify=False)
    sci_as = br.page.find_all('a', href=re.compile('sci-hub'))
    sci_urls = [a['href'] for a in sci_as if 'sci-hub.tech' not in a['href']]

    return sci_urls

def get_working_url(urls):
    """
    Return from urls list one valid URL
    """

    for url in urls:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            return url

def dl_pdf(doi):
    """
    Try to download pdf using scihub
    """

    notify('Trying to retrieve pdf via scihub...')

    #  valid_url = get_working_url(get_scihub_urls())

    with open(os.environ['QUTE_FIFO'], 'w') as fifo:
        fifo.write(f'open -t https://sci-hub.ru/{doi}')
