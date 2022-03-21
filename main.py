#!/usr/bin/env python3
import argparse
from log_processor import CookieLogProcessor

parser = argparse.ArgumentParser(description="CookieLog CLI", usage="main.py <filename> -d <date>")
parser.add_argument("filename", help="name of the cookie log csv file")
parser.add_argument("-d", help="date of interest (YYYY-MM-DD)", required=True)

if __name__ == "__main__":
    args = parser.parse_args()
    cookieProc = CookieLogProcessor()
    cookieProc.process_file(args.filename)
    active_cookies = cookieProc.find_active_by_date(args.d)
    if not active_cookies:
        print("No active cookie found on the specified date")
    else:
        for c in active_cookies:
            print(c)