#!/usr/bin/env python3
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2018 Chris McKinney.

import cgi
import cgitb
import os
from os import path

cgitb.enable(logdir=path.join(path.dirname(__file__), "logs"))

import sys
sys.path.append("pydeps")

STS_HEADER = "Strict-Transport-Security: max-age=31536000"

form = cgi.FieldStorage()

if "test" in form:
    cgi.test()
    raise SystemExit(0)

def error(status, message):
    print("Status: {}".format(status))
    print("Content-Type: text/plain")
    print(STS_HEADER)
    print()
    print("Error: {}".format(message))
    raise SystemExit(0)

def commondir(paths):
    prefix = path.commonprefix(paths)
    index = prefix.rfind("/")
    if index == -1:
        return prefix
    return prefix[:index]

root = os.environ.get("DOCUMENT_ROOT")
if root is None:
    error(500, "DOCUMENT_ROOT not provided.")
url = os.environ.get("SCRIPT_URL", "")
script = os.environ.get("SCRIPT_NAME", "")
common = commondir([url, script])
unique = path.relpath(url, common)
pathname = path.join(root, common.lstrip("/"), "pages", unique)
if path.isdir(pathname):
    if not url.endswith("/"):
        print("Location: {}/".format(os.environ.get("SCRIPT_URI", "")))
        error(301, "Redirecting...")
    pathname = path.join(pathname, "index")
elif url.endswith("/"):
    print("Location: {}".format(os.environ.get("SCRIPT_URI", "//")[:-1]))
    error(301, "Redirecting...")
elif url.endswith("/index"):
    print("Location: {}".format(os.environ.get("SCRIPT_URI", "/index")[:-5]))
    error(301, "Redirecting...")
if path.isfile(pathname + ".ts2"):
    pathname += ".ts2"
elif path.isfile(pathname + ".ts1"):
    pathname += ".ts1"
else:
    error(404, "404 Not Found: {}".format(pathname))

print("Content-Type: text/html")
print(STS_HEADER)
print()

import markdown

EXTENSION_LIST = [
        'markdown.extensions.abbr',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.fenced_code',
        'markdown.extensions.footnotes',
        'markdown.extensions.tables',
        'markdown.extensions.codehilite',
        'markdown.extensions.smarty',
        ]
STYLESHEET_FORMAT = '<link rel="stylesheet" type="text/css" href="{}">'

if pathname.endswith(".ts1"):
    import ts1template
    from urllib import parse
    mdtext = ts1template.render_template(pathname, _GET=dict(form))
    print("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>TachibanaSite</title>
        <link rel="stylesheet" type="text/css"
            href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
    """)
    ts1style_url = path.join(common, "tachibanasite2/ts1style.css")
    print(STYLESHEET_FORMAT.format(parse.quote(ts1style_url)))
    codehilite_url = path.join(common, "tachibanasite2/codehilite.css")
    print(STYLESHEET_FORMAT.format(parse.quote(codehilite_url)))
    print("""
        <link rel="stylesheet" type="text/css"
            href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.10.0/katex.min.css">
        <script type="text/javascript"
            src="https://code.jquery.com/jquery-3.3.1.min.js">
        </script>
        <script type="text/javascript"
            src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js">
        </script>
        <script type="text/javascript"
            src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js">
        </script>
        <script type="text/javascript"
            src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.10.0/katex.min.js">
        </script>
        <script type="text/javascript">
            window.onload = function() {
                $(".katex-math").each(function() {
                    var latex = $(this).text();
                    var html = katex.renderToString(latex);
                    $(this).html(html);
                });
                $(".katex-display").each(function() {
                    var latex = $(this).text();
                    var html = katex.renderToString(latex, {displayMode: true});
                    $(this).html(html);
                });
            }
        </script>
    </head>
    <body>
        <main id="container" class="container" role="main">
            <div id="content" class="markdown-content ts1-content">
    """)
    print(markdown.markdown(mdtext, extensions=EXTENSION_LIST))
    print("""
            </div>
        </main>
    </body>
    </html>
    """)
    raise SystemExit(0)

print("Not Implemented")
