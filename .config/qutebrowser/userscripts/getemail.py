#! /bin/python3

import os
from glob import glob
import sys
import re
from dateutil.parser import parse

from pynvim import attach
from utils import notify, get_nvim_servers

URL = os.path.expandvars('$QUTE_URL')

if 'lkml.iu.edu' in URL:
    PATTERNS = {
        'from': re.compile(r'<!-- name="(.*)"'),
        'date': re.compile(r'<!-- sent="(.*)"'),
        'subject': re.compile(r'<!-- subject="(.*)"'),
        'id': re.compile(r'<!-- id="(.*)"')
    }
elif 'public-inbox' in URL:
    PATTERNS = {
        'from': re.compile(r'From: ([^<>]+)(<[^<>]+>)?$'),
        'date': re.compile(r'Date: (.*)[\t|$]'),
        'subject': re.compile(r'Subject: (.*)$'),
        'id': re.compile(r'Message-ID: <([^<>]+)> \(raw\)$')
    }
elif 'marc.info' in URL:
    PATTERNS = {
        'from': re.compile(r'From:\s+([^<>]+)(<[^<>]+>)?$'),
        'date': re.compile(r'Date:\s+(.*)$'),
        'subject': re.compile(r'Subject:\s+(.*)$'),
        'id': re.compile(r'Message-ID:\s+<([^<>]+)> \(raw\)$')
    }
else:
    sys.exit(1)

METADATA = dict()

def sanitize_string(string):
    if not isinstance(string, str):
        return string

    string = string.strip()
    string = re.sub(r'&', r'\&', string)
    string = re.sub(r'_', r'\_', string)

    return string

with open(os.path.expandvars('$QUTE_TEXT'), 'r') as page_f:
    for _, line in enumerate(page_f):
        for field, pattern in PATTERNS.items():
            MATCH = re.search(pattern, line)
            if MATCH and not field in METADATA:
                METADATA[field] = MATCH.group(1).strip()

if 'date' in METADATA:
    try:
        email_date = parse(METADATA['date'])
        METADATA['date'] = email_date.strftime('%Y-%m-%dT%H:%M:%S')
    except:
        pass

if 'id' in METADATA:
    METADATA['id'] = sanitize_string(METADATA['id'])
else:
    METADATA['id'] = URL

METADATA['url'] = os.path.expandvars('$QUTE_URL')

NVIM_SOCKETS = get_nvim_servers()

for socket in NVIM_SOCKETS:
    nvim = attach('socket', path=socket)
    if re.search('emails.bib', nvim.command_output('buffers')):
        nvim.vars['bibdata'] = METADATA
        nvim.command('call bib#addEmailRef()')
        sys.exit(0)
