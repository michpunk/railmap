#!/bin/python

import argparse
import datetime
import urllib
import urllib2
import cookielib
import time

def main():
  parser = argparse.ArgumentParser(description='Fetch journeys from ORIG to DEST at given DATE and TIME')
  parser.add_argument('orig', metavar='ORIG',
    help='station of departure')
  parser.add_argument('dest', metavar='DEST',
    help='station of origin')
  parser.add_argument('date', metavar='DATE',
    help='date of journey, e.g. 2010/12/01')
  parser.add_argument('time', metavar='TIME',
      help='time of journey, e.g. 18:00')
  args = parser.parse_args()
  orig = args.orig
  dest = args.dest
  time = args.time
  date = datetime.datetime.strptime(args.date, "%Y/%m/%d").date()

  ## TODO Convert time and date
  fetch (orig, dest, date, time)

def fetch(orig, dest, date, t):

  url = swt_url(orig, dest, date, t)

  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  response = opener.open(url)

  check_url = "http://tickets.eastcoast.co.uk/ec/en/JourneyPlanning/CheckForFTAEnquiryCompletion.aspx"

  response = opener.open(check_url)
  time.sleep(2)
  response = opener.open(check_url)

  print response.read()

def get_session_id(response)
  cont = response.read()
#TODO! finish this.

def swt_url(orig, dest, date, time):
  base_url = "https://tickets.eastcoast.co.uk/ec/en/Landing/tis.aspx"
  data = {}
  data['od'] = orig
  data['dd'] = dest
  data['outd'] = str(date.day)
  data['outm'] = str(date.month)
  data['outda'] = 'y'
  data['outh'] = '05'
  data['outmi'] = '00'
  url_values = urllib.urlencode(data)
  full_url = base_url + '?' + url_values
  return full_url

if __name__ == '__main__':
      main()
