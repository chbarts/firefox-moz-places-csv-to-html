#!/usr/bin/env python3

import os
import sys
import csv
import html
import time
import argparse

def csv2html(inf, outf, dtitle):
    outf.write("<!DOCTYPE html>\n")
    outf.write("<html><head><meta charset=\"utf-8\"><title>{}</title></head><body>\n".format(html.escape(dtitle)))
    outf.write("<ul>\n")
    reader = csv.DictReader(inf)
    for row in reader:
        if len(row['url']) == 0:
            continue
        title = row['url']
        if len(row['title']) > 0:
            title = row['title']
        if len(row['last_visit_date']) > 0:
            lvd = int(row['last_visit_date']) / 1000000
            ltime = time.localtime(lvd)
            stime = html.escape(time.strftime("%A, %B %d, %Y %T %z", ltime))
            outf.write("<li>{} &mdash; <a href=\"{}\">{}</a></li>\n".format(stime, html.escape(row['url'], quote=True), html.escape(title)))
        else:
            outf.write("<li><a href=\"{}\">{}</a></li>\n".format(html.escape(row['url'], quote=True), html.escape(title)))
    outf.write("</ul>\n")
    outf.write("</body></html>\n")

parser = argparse.ArgumentParser(description='Convert A Firefox moz_places Table CSV Dump to HTML')

parser.add_argument('-i', '--input', metavar='INFILE', type=str, nargs=1, default='', help='Specify INFILE as RSS input file, defaults to stdin')
parser.add_argument('-o', '--output', metavar='OUTFILE', type=str, nargs=1, default='', help='Specify OUTFILE as HTML output file, defaults to stdout')
parser.add_argument('-t', '--title', metavar='TITLE', type=str, default='Firefox Places Dump', help='The title of the HTML file')

args = parser.parse_args()

if (len(args.input) > 0) and (len(args.output) > 0):
    with open(args.input[0]) as inf:
        with open(args.output[0], 'w') as outf:
            csv2html(inf, outf, args.title)
    sys.exit(0)
elif len(args.input) > 0:
    with open(args.input[0]) as inf:
        csv2html(inf, sys.stdout, args.title)
    sys.exit(0)
elif len(args.output) > 0:
    with open(args.output[0], 'w') as outf:
        csv2html(sys.stdin, outf, args.title)
    sys.exit(0)
else:
    csv2html(sys.stdin, sys.stdout, args.title)
    sys.exit(0)
