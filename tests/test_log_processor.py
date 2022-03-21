import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import log_processor
import pytest

def test_update_top_cookies():
    processor = log_processor.CookieLogProcessor()
        
    # Handles empty daily_map without crashing or
    # non-necessary entries in the date_cookie_map
    daily_map = {}
    date = "0000-00-00"
    processor.update_top_cookies(daily_map, date)
    assert processor.date_cookie_map.get(date, None) == None
    
    # Handles single most active cookie
    daily_map = {'1': 5, '2': 4}
    date = "0000-00-01"
    processor.update_top_cookies(daily_map, date)
    assert processor.date_cookie_map.get(date, None) == ['1']

    # Handles multiple cookies tied at first place
    daily_map = {'1': 5, '2': 5, '3': 5, '4': 4}
    date = "0000-00-02"
    processor.update_top_cookies(daily_map, date)
    assert processor.date_cookie_map.get(date, None) == ['1', '2', '3']

def test_find_active_by_date():
    processor = log_processor.CookieLogProcessor()
    
    # Handles non-existent date
    date = "3 billion yrs BC"
    assert processor.find_active_by_date(date) == None

def test_integration_basics():
    processor = log_processor.CookieLogProcessor()

    # Sample cookie_log.csv
    processor.process_file("../data/cookie_log.csv")
    assert processor.find_active_by_date("2018-12-08") \
        == ["SAZuXPGUrfbcn5UA", "4sMM2LxV07bPJzwf", "fbcn5UAVanZf6UtG"]
    assert processor.find_active_by_date("2018-12-09") \
        == ["AtY0laUfhglK3lC7"]
    assert processor.find_active_by_date("2018-13-00") \
        == None

    # Does not crash with non-existent file
    processor.process_file("../data/i dont exist")

    # Handles empty file
    processor.process_file("../data/empty.csv")

def test_integration_ill_formatted():
    processor = log_processor.CookieLogProcessor()

    # Does not crash when facing ill-formatted lines
    processor.process_file("../data/ill_formatted.csv")

    # Bad format (in data/ill_formatted.csv) include:
    #   1. empty line in the middle and end of file
    #   2. lines with no comma delimiter
    #   3. lines with timestamp length != proper length
    # Note: we treat a line as legal, if it has correct delimiter and correct date length

    # Correctly processed well-formatted lines
    assert processor.find_active_by_date("2018-12-09") \
        == ["SAZuXPGUrfbcn5UA"]
    assert processor.find_active_by_date("2018-12-08") \
        == ["SAZuXPGUrfbcn5UA", "4sMM2LxV07bPJzwf"]

    # Ignores ill-formatted lines
    assert processor.find_active_by_date("2018-12-07") \
        == None




