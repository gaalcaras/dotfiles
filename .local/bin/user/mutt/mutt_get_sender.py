#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#macro index ,f "$my_pipe_start mutt_get_sender.py $my_pipe_end" 'Filter to same sender'
"""

import email
import re
import chardet

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

with open(0, 'rb') as f:
    STDIN = f.read()

enc = chardet.detect(STDIN)
MUTT_OUTPUT = STDIN.decode(enc['encoding'])

MESSAGE = email.message_from_string(MUTT_OUTPUT)
SENDER = get_sender(MESSAGE)

with open('/tmp/neomutt_filter', 'w') as f:
    f.write(f'set my_sender = {SENDER}\n')
    f.write(f'macro index,pager .. "<limit>~f {SENDER}<enter>"\n')
