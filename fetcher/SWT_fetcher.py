#!/usr/bin/python
import sys
import cookielib, urllib2
import argparse
import SWT_parser

from bs4 import BeautifulSoup
from datetime import date
from dateutil.relativedelta import relativedelta

# Gather our code in a main() function
def main():
  parser = argparse.ArgumentParser(description='Fetch prices from given station')
  parser.add_argument('source_station', metavar='STATION',
    help='station to fetch prices from')
  parser.add_argument('list_file', metavar='LIST.txt',
    help='file with the list of stations')
  args = parser.parse_args()
  src = args.source_station
  listfile = args.list_file
  prices = {}
#Get List of stations somewhere
  list_of_stations = get_list_of_stations(listfile)
  if src not in list_of_stations:
    print "Error! Station not in list"
    sys.exit(1)
  sortedstations = list_of_stations.sort()
  for dest in list_of_stations:
    price = fetch_price(src, dest)
    prices[dest] = price
    if (price > 0):
      print '"' + dest + '"' + ':' + str(prices[dest]) + ','

def get_list_of_stations(listfile):
  with open(listfile) as f:
    content = f.readlines()
    content = [x.strip('\n') for x in content]
  return content

def fetch_price(src, dest):
  if src == dest:
    return 0
  page = get_page(src,dest)
  return parse_page(page)

def get_page(src, dest):
  two_months = date.today() + relativedelta( months = +1 )
  d = str(two_months.day)
  m = str(two_months.month)
  y = str(two_months.year)
  url1 = "https://www.buytickets.southwesttrains.co.uk/DataPassedIn.aspx?ori=" \
      + src + "+&dest=" + dest + "+&outDate="+ d + "%2f" + m + "%2f" + y \
      +"&outHourField=11&outMinuteField=30&noa=1&noc=0&rcCode=YNG&rcNum=1"
  url2 = """http://www.buytickets.southwesttrains.co.uk/CheaperSlowerTrains.aspx?Command=FindCheaperTrains"""
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  response = opener.open(url1)
  response = opener.open(url2)
  return response.read()

def parse_page(page):
  soup = BeautifulSoup(page)
  # We need the second instance of 'padded price' attribute
  matches = soup.body.find_all("span", attrs={"class": "padded price"})
  if len(matches) > 1:
    return float(matches[1].text[1:])
  else:
    return -1

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
      main()
