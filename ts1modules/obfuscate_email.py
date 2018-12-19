# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2016 Chris McKinney.

import re
from urllib.parse import quote

EMAIL_OBFUSCATION_COUNTER = 1024
EMAIL_RE = re.compile(r'(mailto:)?[a-zA-Z0-9._\-]+@[a-zA-Z0-9._\-]+')

def obfuscate_email(email_string, html_mode=False):
    '''Obfuscate a string.'''
    global EMAIL_OBFUSCATION_COUNTER
    import urllib
    EMAIL_OBFUSCATION_COUNTER += 15
    obfct = lambda: ''.join([chr((ord(c) + 32) ^ 0x3a)
        for c in str(EMAIL_OBFUSCATION_COUNTER)])
    return ('@@' + obfct() + ('<code>' if html_mode else '``')
            + quote(''.join([chr(ord(c) ^ 0x1f) for c in email_string]))
            + ('</code>' if html_mode else '``') + obfct() + '@@')

def obfuscate_emails(page_seg):
    '''Obfuscate the email addresses in a string.'''
    output = ""
    prev_end = 0
    for match in EMAIL_RE.finditer(page_seg):
        output += page_seg[prev_end:match.start()]
        output += obfuscate_email(match.group())
        prev_end = match.end()
    output += page_seg[prev_end:]
    return output
