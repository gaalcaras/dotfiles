#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Save all attachments inside a specific directory structure :
# yy-mm/sender name/attachments
#
# Message is piped directly from neomutt
#
# Add this to your .muttrc:
# macro index,pager X "<pipe-message>save_all_attachments.py<enter>"
"""


import email
import os
import sys
from datetime import datetime
from email.header import decode_header

DOWNLOAD_DIR = os.path.join('inbox', 'downloads', 'mutt')

def gen_download_dir_path(msg):
    """Generate a directory for the attachments: YYYY-mm/sender"""
    date_str = msg['Date']
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        except ValueError:
            date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z (%Z)')
    date_formatted = date_obj.strftime('%y-%m')

    return os.path.join(DOWNLOAD_DIR, date_formatted, msg['From'])

def decode_filename(file_name):
    """Decoding the filename of the attachment"""
    parts = decode_header(file_name)
    decoded = ''
    for fn_part in parts:
        if isinstance(fn_part[0], bytes):
            # Decode bytes to string using utf-8
            decoded += fn_part[0].decode(fn_part[1])
        else:
            decoded += fn_part[0]
    return decoded

# Get the message from standard input
message = email.message_from_file(sys.stdin)
message_dir = gen_download_dir_path(message)
os.makedirs(message_dir, exist_ok=True)

for part in message.walk():
    # If the part is an attachment
    if part.get_content_disposition() and part.get_content_disposition().startswith('attachment'):
        filename = part.get_filename()

        if filename:
            filename_decoded = decode_filename(filename)

            with open(os.path.join(message_dir, filename_decoded), 'wb') as f:
                # Write the contents of the attachment to the file
                f.write(part.get_payload(decode=True))
