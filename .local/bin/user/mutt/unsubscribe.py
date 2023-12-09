#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Try to automatically unsubscribe from an email newsletter.
#
# Add this to your .muttrc:
# macro index,pager U "<pipe-message>unsubscribe.py<enter>"
"""

import sys
import re
import email
import chardet
from bs4 import BeautifulSoup
from subprocess import call, Popen, PIPE

# Strings to match
UNSUB_STRINGS = (
    'unsubscrib',
    'subscription',
    'ne plus recevoir',
    'désabonne',
    'désinscrire',
    'abonnement',
    'notification'
)

def get_msg_body(message):
    """Return message body"""

    html = ""

    for part in message.walk():
        if part.get_content_type() == "text/html":
            try:
                html += part.get_payload(decode=True).decode('utf-8')
            except UnicodeDecodeError:
                encoding = chardet.detect(part.get_payload(decode=True))
                html += part.get_payload(decode=True).decode(encoding['encoding'])
        else:
            print(f'No support the "{part.get_content_type()}" content type (yet).')

    return BeautifulSoup(html, 'html.parser')

def get_sender(message):
    """Return the email of the sender"""

    from_field = message['From']

    # Decode from_field
    from_field = email.header.decode_header(from_field)[-1][0]
    if not isinstance(from_field, str):
        try:
            from_field = from_field.decode('utf-8')
        except UnicodeDecodeError:
            from_field = from_field.decode(chardet.detect(from_field)['encoding'])

    from_field_pat = re.compile(r'<(.*)>')
    if from_field_pat.search(from_field):
        from_field = from_field_pat.search(from_field).group(1)

    return from_field

def go_to_unsub(link):
    print(f"Opening link: {link.attrs['href']}")
    call(['qutebrowser', link.attrs['href']])
    return True

def unsubscribe(message):
    soup = get_msg_body(message)

    if not soup:
        return

    unsub_p = re.compile("(" + '|'.join(UNSUB_STRINGS) + ")", re.I)
    match = list()

    # Strategy 1: look for pattern in the string of the links
    match.extend(soup("a", string=unsub_p))

    # Strategy 2: look for pattern in the href of the links
    if not match:
        match.extend(soup("a", href=unsub_p))

    # Strategy 3: look for pattern in the text of children of the links
    if not match:
        for link in soup("a"):
            if unsub_p.search(link.text):
                match.append(link)

    # Strategy 4: look for pattern everywhere and get links contained in matching nodes
    if not match:
        for node in soup(text=unsub_p):
            for link in node.find_next_siblings("a"):
                match.append(link)

    if match:
        go_to_unsub(match[-1])
    else:
        print('Could not find way to unsubscribe from this newsletter. Sorry!')

    with open('/tmp/neomutt_filter', 'w') as mutt_f:
        sender = get_sender(message)
        mutt_f.write(f'set my_sender = {sender}\n')
        mutt_f.write(f'macro index,pager .. "<limit>~f {sender}<enter>"\n')

# Read from stdin without using sys module, which will fail sometimes if
# encoding is unpredictable.
# See: https://stackoverflow.com/questions/53026131/how-to-prevent-unicodedecodeerror-when-reading-piped-input-from-sys-stdin/53028829
try:
    with open(0, 'rb') as f:
        STDIN = f.read()

    enc = chardet.detect(STDIN)
    if enc['encoding']:
        MUTT_OUTPUT = STDIN.decode(enc['encoding'])
    else:
        MUTT_OUTPUT = STDIN.decode('utf-8')
except UnicodeDecodeError:
    MUTT_OUTPUT = sys.stdin.read()

MESSAGE = email.message_from_string(MUTT_OUTPUT)
unsubscribe(MESSAGE)
